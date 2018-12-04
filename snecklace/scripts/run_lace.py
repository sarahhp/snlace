"""Run Lace to create the combined superTranscriptome"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-11-02"

#include: "cluster.py"

OUTPUT_DIR = "output_data/"
ST_OUTDIR = "superT"

DATASET = config["dataset"]
#configfile: "necklace.json"

rule run_lace:
    version: "3.4"
    input:
        seqs = OUTPUT_DIR + "clustering/" + DATASET + "_sequences.fa",
        clusters = OUTPUT_DIR + "clustering/" + DATASET + ".clusters"
    conda: "../envs/lace.yml"
    threads: config["max_threads"]
    benchmark: ST_OUTDIR + "/10lace.times.tab"
    output:
        ST_OUTDIR + "/" + DATASET + "_SuperDuper.fa"
    shell:
        "Lace.py --cores {threads} "
            "--tidy "
            "--outputDir {ST_OUTDIR} "
            "{input.seqs} {input.clusters} ;"
        "mv {ST_OUTDIR}/SuperDuper.fasta {ST_OUTDIR}/{DATASET}_SuperDuper.fa "
