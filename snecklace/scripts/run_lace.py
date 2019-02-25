"""Run Lace to create the combined superTranscriptome"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-12-17"

#include: "cluster.py"

OUTPUT_DIR = "output_data/"
ST_OUTDIR = "superT"

DATASET = config["dataset"]
#configfile: "necklace.json"

rule run_lace:
    version: "3.6"
    input:
        seqs = "clustering/" + DATASET + "_sequences.fa",
        clusters = "clustering/" + DATASET + ".clusters"
    params:
        config["params"]["lace"]
    conda: "../envs/lace.yml"
    threads: config["max_threads"]
    benchmark: ST_OUTDIR + "/10lace.times.tab"
    output:
        final = ST_OUTDIR + "/" + DATASET + "_SuperDuper.fa",
        working = directory(ST_OUTDIR + "/SuperFiles")
    shell:
       # "conda upgrade matplotlib -y; "
        "Lace.py --cores {threads} {params} "
           # "--tidy "
            "--outputDir {output.working} "
            "{input.seqs} {input.clusters} ;"
        "mv {output.working}/SuperDuper.fasta {output.final} ;"
        "mv {output.working}/SuperDuper.gff {ST_OUTDIR}/SuperDuper.gff "
