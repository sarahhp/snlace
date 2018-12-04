"""de novo transcriptome assembly from RNAseq reads using Trinity
      1. Run Trinity
      2. Clean files and calculate useful statistics
"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-11-02"

OUTPUT_DIR = "output_data/"
DA_OUTDIR = OUTPUT_DIR + "de_novo_assembly/"

#configfile: "necklace.json"
DATASET = config["dataset"]
TRINITY_HOME = config["home_dirs"]["trinity"]

rule de_novo_assembly:
    version: "3.4"
    input:
        reads_R1 = expand ("{path}/{sample}_{pair_notation}1{suffix}",
                           path = config["fastq_dir"],
                           sample = config["samples"],
                           pair_notation = config["pair_notation"],
                           suffix = config["fastq_suffix"]),
        reads_R2 = expand ("{path}/{sample}_{pair_notation}2{suffix}",
                           path = config["fastq_dir"],
                           sample = config["samples"],
                           pair_notation = config["pair_notation"],
                           suffix = config["fastq_suffix"])
    params:
        extra = config["params"]["trinity"],
        #formatted hisat inputs
        R1 = lambda wildcards, input: ",".join(input.reads_R1),
        R2 = lambda wildcards, input: ",".join(input.reads_R2),
    threads: config["max_threads"] - 1
    benchmark: DA_OUTDIR + "06trinity.times.tab"
    output:
        "trinity_out_dir.Trinity.fasta"
    shell:
        "Trinity --seqType fq {params.extra} "
            "--left {params.R1} --right {params.R2} "
            "--CPU {threads} --full_cleanup "

rule clean_de_novo:
    version: "3.1"
    input:
        "trinity_out_dir.Trinity.fasta"
    params:
        trinity_stats = TRINITY_HOME + "/util/TrinityStats.pl"
    output:
        sum_file = DA_OUTDIR + DATASET + "_de_novo.sum.txt",
        de_novo = DA_OUTDIR + DATASET + "_de_novo.fa"
    shell:
        "mv {input} {output.de_novo} ;"
        "{params.trinity_stats} {output.de_novo} > {output.sum_file} ;"
        "mv trinity_out_dir.Trinity.fasta.gene_trans_map {DA_OUTDIR} "
