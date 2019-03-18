"""Build superTranscriptome from the genome/annotation of species
   related to the study species.
      1. Merge gene annotations (stringtie --merge) 
      2. Flatten gtf (custom tool gtf2flatgtf from Oshlack pipeline)
      3. Extract exons from fasta (gffread)
"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-12-17"

import os

TOOLS= config["home_dirs"]["tools"]

#configfile: "necklace.json"
SP_NAMES = config["relatedsp_names"]
RELSP_OUTDIR = config["relatedsp_superT_dir"] + "/" + SP_NAMES + "/"

rule merge_related_annotations:
    version: "3.3"
    input:
        related_annots = config["relatedsp_annot_files"]
    params:
        config["params"]["stringtie_merge"]
    benchmark: RELSP_OUTDIR + "05merge_relsp.times.tab"
    output:
        combined = RELSP_OUTDIR + SP_NAMES + "_combined.gtf",
        merged_annot = RELSP_OUTDIR + SP_NAMES + "_merged.gtf",                           
    shell:
        "cat {input.related_annots} > {output.combined} ;"
        "stringtie --merge {params} -G {output.combined} "
             "-o {output.merged_annot} {input.related_annots} "

rule flatten_related_gtfs:
    version: "3.0"
    input:
        RELSP_OUTDIR + SP_NAMES + "_merged.gtf",
    output:
        RELSP_OUTDIR + SP_NAMES + "_merged.flat.gtf",
    shell:
        "{TOOLS}/gtf2flatgtf {input} {output} "

rule extract_exons_from_related_fasta:
    version: "3.2"
    input:
        flat_gtf = RELSP_OUTDIR + SP_NAMES + "_merged.flat.gtf",
        genome = config["relatedsp_genome_file"]
    output:
        superT = RELSP_OUTDIR + SP_NAMES + "_superT.fa",
    shell:
        "gffread {input.flat_gtf} -g {input.genome} -w {output.superT}"
