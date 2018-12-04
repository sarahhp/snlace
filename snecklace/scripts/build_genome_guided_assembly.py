""" Build genome guided assembly from paired-end RNAseq data and
    reference genome/annotation
       1. build genome index (hisat2 tool)
       2. build splice site index from gtf (hisat2 tool)
       3. map reads to genome with hisat2
       4. assemble transcriptome with stringtie
"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-11-02"

import os

GGA_OUTDIR = "genome_guided_assembly/"

#configfile: "necklace.json"
DATASET = config["dataset"]
GENOME_NAME = config["genome_name"]
GENOME_INDEX = config["genome_dir"] + "/index/" + GENOME_NAME

rule build_genome_index:
    version:"3.4"
    input:
        genome_file = expand ("{genome_dir}/{file_name}", 
                               genome_dir = config["genome_dir"],
                               file_name = config["genome_file"])
    params:
        config["params"]["hisat-build"]
    benchmark: GGA_OUTDIR + "01genome_index.times.tab"
    output:
        genome_idx = GENOME_INDEX + ".1.ht2l"
    shell:
        "hisat2-build {params} --large-index {input.genome_file} {GENOME_INDEX} "

rule gtf_to_splice_sites:
    version: "3.0"
    input:
        annots = config["annot_files"]
    output:
        splicesite_idx = expand ("{annot_dir}/{genome_name}.splicesites",
                                 annot_dir = os.path.dirname (config["annot_files"][0]),
                                 genome_name = GENOME_NAME)
    shell:
        "cat {input.annots} | "
            "hisat2_extract_splice_sites.py - > {output.splicesite_idx} "


rule map_reads_to_genome:
    version: "3.0"
    input:    
        genome_idx = GENOME_INDEX + ".1.ht2l",
        splicesite_idx = expand ("{annot_dir}/{genome_name}.splicesites",
                                 annot_dir = os.path.dirname (config["annot_files"][0]),
                                 genome_name = GENOME_NAME),
        #fastq files
        reads_R1 = expand ("{path}/{sample}_{pair_notation}1{suffix}", 
                           path = config["fastq_dir"], 
                           sample = config["samples"],
                           pair_notation = config["pair_notation"],
                           suffix = config["fastq_suffix"] ),
        reads_R2 = expand ("{path}/{sample}_{pair_notation}2{suffix}",
                           path   = config["fastq_dir"],
                           sample = config["samples"],
                           pair_notation = config["pair_notation"],
                           suffix = config["fastq_suffix"] )
    params:
        extra = config["params"]["hisat_initial"],
        #formatted hisat inputs
        R1 = lambda wildcards, input: ",".join(input.reads_R1),
        R2 = lambda wildcards, input: ",".join(input.reads_R2),
    benchmark: GGA_OUTDIR + "02hisat2.times.tab"
    output:
        novel_ss = GGA_OUTDIR + DATASET + "_novel.splicesites", 
        summary  = GGA_OUTDIR + DATASET + ".sum.txt",
        bam_file = GGA_OUTDIR + DATASET + ".sorted.bam"
    shell:
        "hisat2 {params.extra} "
            "--known-splicesite-infile {input.splicesite_idx} "
            "--novel-splicesite-outfile {output.novel_ss} "
            "--dta "
            "    --summary-file {output.summary} "
            "-x {GENOME_INDEX} "
            "-1 {params.R1} -2 {params.R2} "
        " | samtools view -Su - "
        " | samtools sort - -o {output.bam_file} "
        
rule genome_assembly:
    version: "3.0"
    input:
        bam_file = GGA_OUTDIR + DATASET + ".sorted.bam"
    params:
        config["params"]["stringtie"]
    benchmark: GGA_OUTDIR + "03stringtie_assembly.times.tab"
    output:
        assembly = GGA_OUTDIR + DATASET + "_assembly.gtf"
    shell:
        "stringtie {input.bam_file} -o {output.assembly} {params}"
