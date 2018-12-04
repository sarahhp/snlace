"""Use feature counts to quantify the reads per "block" and per gene
      1. Get splice blocks annotation (samtools, bash one-liner and
      custom tool make_blocks from Oshlack pipeline)
      2. Count reads applied to each block/gene (subread's featureCounts)
"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-11-02"

#include: "map_reads_to_superT.py"

TOOLS = "tools"
OUTPUT_DIR = "output_data/"
COUNT_OUTDIR = OUTPUT_DIR  + "counts/"

#configfile: "necklace.json"
DATASET = config["dataset"]

rule get_splice_blocks:
    version: "3.0"
    input:
        superT = OUTPUT_DIR + "superT/" + DATASET + "_SuperDuper.fa",
        splicesites = expand (OUTPUT_DIR + "mapped_reads/{sample}.splicesites",
                                         sample = config["samples"]) 
    output:
        gene_sizes = COUNT_OUTDIR + "gene.sizes",
        blocks = COUNT_OUTDIR +  DATASET + "_blocks.gtf"
    shell:
        "samtools faidx {input.superT} ;"
        "cut -f1,2 {input.superT}.fai > {output.gene_sizes} ;"
        "{TOOLS}/make_blocks {output.gene_sizes} {input.splicesites} "
            "> {output.blocks} " 

rule count_reads:
    version: "3.4"
    input:
        alns = expand (OUTPUT_DIR + "mapped_reads/{sample}.sorted.bam",
                                  sample = config["samples"]),
        blocks = COUNT_OUTDIR + DATASET + "_blocks.gtf"
    params:
        gene_opt = config["params"]["featureCounts_genes"],
        block_opt = config["params"]["featureCounts_blocks"]
    threads: config["max_threads"]-1
    benchmark: COUNT_OUTDIR + "13featurecounts.times.tab"
    output:
        gene = COUNT_OUTDIR + DATASET + "_gene.counts",
        block = COUNT_OUTDIR + DATASET + "_block.counts"
    shell:
        "featureCounts -T {threads} {params.gene_opt} -t exon -g gene_id "
            "-a {input.blocks} -o {output.gene} {input.alns} ;"
        "featureCounts -T {threads} {params.block_opt} -f -t exon -g gene_id "
            "-a {input.blocks} -o {output.block} {input.alns} ;"
