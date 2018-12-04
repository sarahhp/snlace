"""Build superTrancriptome from a transcriptome assembled
   via a genome guided (stringtie) method
      1. Merge gene annotations (stringtie --merge) 
      2. Flatten gtf (custom tool gtf2flatgtf from Oshlack pipeline)
      3. Extract exons from fasta (gffread)
"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-10-02"

#include: "build_genome_guided_assembly.py"

TOOLS = "tools"
OUTPUT_DIR = "output_data/"
GGST_OUTDIR = OUTPUT_DIR + "genome_superT/"

#configfile: "necklace.json"
DATASET = config["dataset"]

rule merge_genome_annotations:
    version: "3.2"
    input:
        annots = config["annot_files"],
        cust_annot = OUTPUT_DIR + "genome_guided_assembly/" + DATASET + "_assembly.gtf"
    params:
        config["params"]["stringtie_merge"]
    benchmark: GGST_OUTDIR + "04merge_gga.times.tab"
    output:
        merged_genomes = GGST_OUTDIR + DATASET + "_genome_merged.gtf"
    shell:
        "stringtie --merge {params} -G {input.annots} "
            "-o {output.merged_genomes} {input.cust_annot} {input.annots} "
        
rule flatten_gtf:
    version: "3.0"
    input:                                                                          
        GGST_OUTDIR + DATASET + "_genome_merged.gtf"
    output:
        GGST_OUTDIR + DATASET + "_genome_merged.flat.gtf"
    shell:
        "{TOOLS}/gtf2flatgtf {input} {output}"
         

rule extract_exons_from_fasta:
    version: "3.0"
    input:
        flat_gtf = GGST_OUTDIR + DATASET + "_genome_merged.flat.gtf",
        g_file = expand ("{genome_dir}/{genome_file}",
                          genome_dir = config["genome_dir"],
                          genome_file = config["genome_file"])
    output:
        superT = GGST_OUTDIR + DATASET + "_genome_superT.fa"
    shell:
        "gffread {input.flat_gtf} -g {input.g_file} -w {output.superT}"
