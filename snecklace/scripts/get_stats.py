"""A new version of get_stats.py
   Uses a series of small python scripts to gather some useful
   statistics into a single tab delimited file. 
      1. Collate hisat summaries for each sample, calculating averages
      2. Collate featurecounts of genes and blocks
      3. Combine novel splicesites files from hisat output
      4. Create table with the following fields:
         - no.genes
         - no supported genes
         - transciptome size
         - alignment rate (%)
         - UniqueCon rate (%)
         - Unique non-Con rate (%)
         - Multimapping rate (%)
         - Reads assigned to reads 
         - Novel splicesites found
      5. Create supplementary table of details on the de novo assembly
      and the related species superT with the follwowing info:
         - No. genes relatedsp
         - Relatedsp transcriptome size (bp)
         - No. genes de novo assembly
         - De novo assembly size (bp)
"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-11-12"

import os
import sys
import Bio.Seq
import pandas as pd

#custom helper scripts
sys.path.append("/home/sarah/pkgs/nlace/snlace/snecklace/stats_scripts")
import get_hisat_sum as hisat_sum
import get_fc_sum as fc_sum
import get_no_genes as no_genes
import get_no_bp
import get_fc_sum as fc_sum
from get_denovo_sum import getTrinityStats

#include: "get_counts.py"

OUTPUT_DIR = "output_data/"
STAT_OUTDIR = "stats/"

#configfile: "necklace.json"
DATASET = config["dataset"]

rule get_hisat_summary:
    version: "3.0"
    input:
        map_sum = "mapped_reads/" + config["samples"][0] + ".sum.txt"
    output:
        sum_file = STAT_OUTDIR + DATASET + "_hisat.sum.tab"
    run: 
        hisat_sum.getHisatSummary(datadir=os.path.dirname(input.map_sum), outpath=output.sum_file)

rule get_featureCounts:
    version: "3.0"
    input:
        blocks = "counts/" + DATASET + "_block.counts",
        genes = "counts/" + DATASET + "_gene.counts"
    output:
        sum_file = STAT_OUTDIR + DATASET + "_fc.sum.tab"
    run:
        fc_sum.getFeatureSummary(datadir=os.path.dirname(input.blocks), outpath=output.sum_file)


rule novel_splicesites:
    version: "3.0"
    input:
        expand ("mapped_reads/{sample}.splicesites",
                sample =  config["samples"])
    output:
        STAT_OUTDIR + DATASET + ".splicesites"
    shell:
        "cat {input} | sort -u > {output}"

rule superT_stats:
    version: "3.0"
    input:
        gtf = "counts/" + DATASET + "_blocks.gtf",
        gene_counts = "counts/" + DATASET + "_gene.counts",
        fasta = "superT/" + DATASET + "_SuperDuper.fa",
        hisat = STAT_OUTDIR + DATASET + "_hisat.sum.tab",
        fc = STAT_OUTDIR + DATASET + "_fc.sum.tab",
        splice_file = STAT_OUTDIR + DATASET + ".splicesites"
    output:
        sum_file = STAT_OUTDIR + DATASET + ".sum.tab"
    run:
        #values created by helper scripts
        genes = no_genes.get_no_superT_genes (input.gtf)
        supp_genes = no_genes.file_len (input.gene_counts) - 2 #account for header lines
        size = get_no_bp.bp_in_fasta(input.fasta)
        alns = pd.read_table(input.hisat).iloc[-1,1:]
        assign_reads = pd.read_table(input.fc).iloc[1,1]
        no_novel_ss = no_genes.file_len (input.splice_file)
        
        idx = ["No. genes", "No. supported genes", "Transcriptome Size (bp)", \
               "Total Alignment rate", "Concordant, unique", \
               "Not-concordant, unqiue", "Multimapping", \
               "No. assigned reads", "No. novel splicesites"]
        data = [genes, supp_genes, size, alns[1], alns[2], alns[3], alns[4], \
                assign_reads, no_novel_ss]
        table = pd.DataFrame(data, index=idx, columns=["SuperT"])
        table.to_csv(output.sum_file, sep='\t', header=True, index=True)
     
rule related_denovo_stats:
    version: "3.0"
    input:
        denovo_stats = "de_novo_assembly/" + DATASET + "_de_novo.sum.txt",
        relsp_gtf = expand ("{superTdir}/{species}/{species}_combined.gtf",
                        superTdir =config["relatedsp_superT_dir"],
                        species = config ["relatedsp_names"]),
        relsp_fasta = expand ("{superTdir}/{species}/{species}_superT.fa",
                        superTdir =config["relatedsp_superT_dir"],
                        species = config ["relatedsp_names"])
    output:
        sum_file = STAT_OUTDIR + DATASET + "_rel_denovo.sum.tab"
    run:
        denovo = getTrinityStats (input.denovo_stats)
        relsp_genes = no_genes.get_no_annot_genes(input.relsp_gtf[0])
        relsp_bp = get_no_bp.bp_in_fasta(input.relsp_fasta[0])

        idx = ["No. genes relatedsp", "Relatedsp transcriptome size (bp)", \
               "No. genes de novo assembly", "De novo assembly size (bp)"]
        table = pd.DataFrame([relsp_genes, relsp_bp, denovo[0], denovo[1]], index = idx)
        table.to_csv(output.sum_file, sep='\t', header=True, index=True)
     
rule time_stats:
    '''Collates time and memory usage information from main rules from pipeline.
    This information was collected by snakemake's benchmark capability and
    stored in files starting with a two-digit number and ending with the
    .times.tab suffix e.g. '01genome_index.times.tab'.  
    '''
    version: "3.4"
    input:
        "counts/" + DATASET + "_gene.counts"
    output:
        time_sum = STAT_OUTDIR + DATASET + ".times.tab"
    run:
        first_file = True
        outdirs = ["genome_guided_assembly", \
                   "genome_superT", "de_novo_assembly", \
                   config["relatedsp_superT_dir"] + "/"  + config["relatedsp_names"], \
                   "clustering", "superT", \
                   "mapped_reads", "counts"] 
        for out in outdirs:
            files = os.listdir(out)
            for path in files:
                if path.endswith(".times.tab"):
                    time_file = open(os.path.join(out,path), "r")
                    lines = list (time_file)
                    time_file.close()
                    
                    if first_file == True:
                        time_sum = open (output.time_sum, "a")
                        time_sum.write("\t" + lines[0])
                        first_file = False
                    
                    description = path.replace(".times.tab", "")
                    line = description + "\t" + lines[1]
                    time_sum.write(line)
        time_sum.close()
    
