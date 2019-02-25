""" Count number of genes found in
    - a gtf annotation (get_no_annot_genes)
    - a transcriptome fasta file (get_no_superT_genes)
    
Also file_len counts the number of lines in a file (useful for counting no.
supported genes from a featureCounts file)
"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-09-27"

import pandas as pd

def get_no_annot_genes(annot):
    attributes = pd.read_table(annot, sep="\t", usecols=[8])
    att_series = attributes.iloc[:,0]
    gene_ids = pd.Series(data=(n.split(sep=';')[0] for n in att_series))
    genes = gene_ids.unique()
    no_genes = len(genes)
    return no_genes

def get_no_superT_genes(superT):
    gene_ids = pd.read_table(superT, sep='\t', usecols=[0], header=None)
    geneid_series = gene_ids.iloc[:,0]
    genes = geneid_series.unique()
    no_genes = len(genes)
    return no_genes

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if __name__ == '__main__':
    annot = "/home/sarah/packages/necklace/demo_data/data/Ovis_aries.Oar_v3.1.90.chr14.gtf"
    superT = "/home/sarah/packages/necklace/stat-test01/counts_stats/demo_blocks.gtf"
    gene_counts = "/home/sarah/packages/necklace/stat-test01/counts_stats/demo_gene.counts"
    stringtie = "/home/sarah/packages/necklace/demo_data/genome_guided_assembly/genome_assembly.gtf"
    n = get_no_annot_genes(stringtie)
    p = get_no_superT_genes (superT)
    supgenes = file_len (gene_counts) - 2 #minus the two header lines
    print("stringtie", n,p)
