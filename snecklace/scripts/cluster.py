"""Clustering of study species genome-guided and related species
   superTranscriptomes, and de novo assembly
      1. Match related species and study species assembly (translated
         DNA sequence using blat)
      2. Match related species and de novo assembly (translated DNA
         sequence using blat)
      3. Match genome guided assembly and de novo assembly (direct DNA
         sequence using blat)
      4. Get gene names (bash one-liner)
      5. Make cluster files for lace (custom tool cluster from
         Oshlack pipeline)
"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-12-17"

#include: "build_genome_superT.py"
#include: "build_de_novo_assembly.py"
#include: "build_relatedsp_superT.py"

TOOLS = config["home_dirs"]["tools"]
OUTPUT_DIR = "output_data/"
CLUSTER_OUTDIR = "clustering/"

#configfile: "necklace.json"
DATASET = config["dataset"]

"""Files from previous workflows:  """
make_genome = "genome_superT/" + DATASET + "_genome_superT.fa" 
make_related = expand ("{rel_dir}/{species}/{species}_superT.fa",
                       rel_dir = config["relatedsp_superT_dir"],
                       species = config["relatedsp_names"])
make_de_novo = "de_novo_assembly/" + DATASET + "_de_novo.fa"

rule blat_relST_genomeST:
    version: "3.0"
    input:
        genome = make_genome,
        related = make_related
    params:
        config["params"]["blat_related"]
    benchmark: CLUSTER_OUTDIR + "07blat_relST_gST.times.tab"
    output:
        CLUSTER_OUTDIR + "relST_genomeST.psl"
    shell:
        "blat {input.related} {input.genome} {params} {output} "

rule blat_relST_denovo:
    version: "3.7"
    input:
        related = make_related,
        de_novo = make_de_novo
    params:
         config["params"]["blat_related"]
    #threads: config["max_threads"]-1
    benchmark: CLUSTER_OUTDIR + "08blat_relST_denovo.times.tab"
    output:
        CLUSTER_OUTDIR + "relST_denovo.psl"
    shell:
        "blat {input.related} {input.de_novo} {params} {output}"

rule blat_genomeST_denovo:
    version: "3.7"
    input:
        genome = make_genome,
        de_novo = make_de_novo
    params:
        config["params"]["blat"]
    threads: config["max_threads"]-1
    benchmark: CLUSTER_OUTDIR + "09blat_gST_denovo.times.tab"
    output:
        CLUSTER_OUTDIR + "genomeST_denovo.psl"
    shell:
        "pblat threads={threads} {params} {input.genome} {input.de_novo} {output}"

rule genome_ST_names:
    version: "3.0"
    input: 
        genome = make_genome
    output:
        CLUSTER_OUTDIR + DATASET + "_superT.names"
    shell:
        "grep \"^>\" {input.genome} | sed 's/>//g' "
            "| cut -f1 -d \" \" > {output}"

rule make_cluster_files_for_lace:
    version: "3.0"
    input:
        gen_denovo = CLUSTER_OUTDIR + "genomeST_denovo.psl",
        rel_denovo = CLUSTER_OUTDIR + "relST_denovo.psl",
        rel_genome = CLUSTER_OUTDIR + "relST_genomeST.psl",
        names = CLUSTER_OUTDIR + DATASET + "_superT.names",
        genome = make_genome,
        de_novo = make_de_novo
    output:
        clusters = CLUSTER_OUTDIR + DATASET + ".clusters",
        seqs = CLUSTER_OUTDIR + DATASET + "_sequences.fa"
    shell:
        "{TOOLS}/cluster {input.gen_denovo} {input.rel_denovo} "
            "{input.rel_genome} {input.names} > {output.clusters} ;"
        "cat {input.genome} {input.de_novo} > {output.seqs} "
