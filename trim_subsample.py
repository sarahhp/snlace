__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-11-15"

""" QC and Trimming with fastp

    Trimming and QC with fastp.
    Then subsampling of reads via seqtk.

    Now starts with a sample/sample.file structure.

    Number of reads to sample is can be supplied via pairs_to_sample
    parameter of the sub_sample rule.  Additional options can be passed
    to fastp via the 'extra' parameter of the fastp rule.

    Now can do multiple subsampling runs from the same script
"""

import random

#configfile: "config.json"

RAW = config["raw_dir"]
NOTATION = config["pair_notation"]
QC = "qc/"
SUB = "qc/subsamples/"
NO_READS = 50000
FASTP_PARAMS = ""

rule all:
    version:
        "3.0"
    input:
        expand(SUB + str(NO_READS) + "/{sample}_{notation}{pair}_subsample.fastq.gz",
            sample = config["samples"],
            notation = NOTATION,
            pair = ["1", "2"])
        
rule fastp_simple_dir:
    """For use when all fastq files are in a single directory.  """
    version:
        "3.5"
    input:
        r1_raw = RAW + "{sample}_{notation}1_001.fastq.gz",
        r2_raw = RAW + "{sample}_{notation}2_001.fastq.gz"
    params:
        extra = FASTP_PARAMS,  
        html = QC + "{sample}.html",
        json = QC + "{sample}.json"
    #onda: "envs/fastp.yml"
    output:
        r1 =   QC + "trimmed/{sample}_{notation}1_trim.fastq.gz",
        r2 =   QC + "trimmed/{sample}_{notation}2_trim.fastq.gz"
    shell:
        "fastp -i {input.r1_raw} -I {input.r2_raw} "
            "-o {output.r1} -O {output.r2} "
            "-h {params.html} -j {params.json} "
            "{params.extra}"

rule fastp_twotier_dirs:
    """For use when fastq files are distributed between directories
       of the same name. e.g. base_dir/{sample}/{sample}.fastq
    """
    version:
        "3.5"
    params:
        extra = FASTP_PARAMS, 
        html = QC + "{sample}.html",
        json = QC + "{sample}.json"
    input:
        r1_raw = RAW + "{sample}/{sample}_{notation}1_001.fastq.gz",
        r2_raw = RAW + "{sample}/{sample}_R2_001.fastq.gz"
    #conda: "envs/fastp.yml"
    output:
        r1 =   QC + "trimmed/{sample}_{notation}1_trim.fastq.gz",
        r2 =   QC + "trimmed/{sample}_{notation}2_trim.fastq.gz"
    shell:
        "fastp -i {input.r1_raw} -I {input.r2_raw} "
            "-o {output.r1} -O {output.r2} "
            "-h {params.html} -j {params.json} "
            "{params.extra}"

rule sub_sample:
    version:
        "4.0"
    input:
        trim_reads1 = QC + "trimmed/{sample}_{notation}1_trim.fastq.gz",
        trim_reads2 = QC + "trimmed/{sample}_{notation}2_trim.fastq.gz"
    params:
        pairs_to_sample = NO_READS
    #conda: "envs/fastp.yml"
    output:
        subsample1 = SUB + str(NO_READS) + "/{sample}_{notation}1_subsample.fastq",
        subsample2 = SUB + str(NO_READS) + "/{sample}_{notation}2_subsample.fastq"
    run:
        seed = random.randrange(10*len(config["samples"]))
        shell("seqtk sample -s{seed} {input.trim_reads1} {params.pairs_to_sample} "
            " > {output.subsample1} \n"
        "seqtk sample -s{seed} {input.trim_reads2} {params.pairs_to_sample} "
            " > {output.subsample2} ")

rule zipper:
    input:
        SUB + str(NO_READS) + "/{sample}_{notation}{pair}_subsample.fastq"
    output:
        SUB + str(NO_READS) + "/{sample}_{notation}{pair}_subsample.fastq.gz"
    shell:
        "gzip {input}"


