""" Map original RNAseq reads back to superTranscriptome using hisat  
       1. build superT index (hisat2 tool)
       2. map reads for each sample to superT (hisat2)
       3. do 2. for all samples
"""
__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-12-17"

#include: "run_lace.py"

OUTPUT_DIR = "output_data/"
MAP_OUTDIR = "mapped_reads/"

#configfile: "necklace.json"
SUPERT_INDEX = MAP_OUTDIR + "indices/" + config["dataset"] + "_superT"

rule build_superT_index:
    version: "3.4"
    input:
        superT = "superT/" + config["dataset"] + "_SuperDuper.fa"
    params:
        config["params"]["hisat-build"]
    benchmark: MAP_OUTDIR + "11superT_index.times.tab"
    output:
        SUPERT_INDEX + ".1.ht2l"
    shell:
        "hisat2-build {params} --large-index {input.superT} {SUPERT_INDEX}"

rule map_reads_to_superT:
    version: "3.4"
    input:
        genome_idx = SUPERT_INDEX + ".1.ht2l",
        #fastq files 
        reads_R1 = config["fastq_dir"] + "/{sample}_" \
                   + config["pair_notation"] + "1" + config["fastq_suffix"], 
        reads_R2 = config["fastq_dir"] + "/{sample}_" \
                   + config["pair_notation"] + "2" + config["fastq_suffix"]
    params:
        config["params"]["hisat_final"]
    threads: int( config["max_threads"] / len(config["samples"]) )
    benchmark: MAP_OUTDIR + "12{sample}.times.tab"
    output:
        summary     = MAP_OUTDIR + "{sample}.sum.txt",
        splicesites = MAP_OUTDIR + "{sample}.splicesites",
        bam_file    = MAP_OUTDIR + "{sample}.sorted.bam",
        bam_index   = MAP_OUTDIR + "{sample}.sorted.bam.bai"

    shell:
        "hisat2 {params} "
            "--threads {threads} "
            "--summary-file {output.summary} "
            "--novel-splicesite-outfile {output.splicesites} "
            	"-x {SUPERT_INDEX} "
                "-1 {input.reads_R1} -2 {input.reads_R2} "
        "| samtools view -Su "
        "| samtools sort - -o {output.bam_file} \n"
        "samtools index {output.bam_file} {output.bam_index} "
        
rule map_all_samples:
    version: "3.0"
    input:
        expand (MAP_OUTDIR + "{sample}.sorted.bam.bai",
                sample = config["samples"])
    


