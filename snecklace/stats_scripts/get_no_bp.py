""" Find transcriptome size in base pairs from gtf and transcriptome
fasta.  bp_in_gtf still in production
"""

__author__ = "Sarah Hazell Pickering (sarah.pickering@anu.edu.au)"
__date__ = "2018-09-27"

import pandas as pd

def bp_in_fasta (fasta):
    bp = 0
    for line in open (fasta):
        if not (line.startswith('>')):
            bp += len(line)
    return bp

def bp_in_gtf (gtf_file):
    gtf = pd.read_table(gtf_file, sep='\t', usecols=[2,3,4,8], header=None,\
                        names=["seqtype", "start", "end", "attributes"])
    '''
    filter_gtf = gtf.loc[gtf['seqtype']=='exon'] #keep only rows that denote an exon
    #gene_ids = pd.Series(data=(n.split(sep=';')[0] for n in filter_gtf.iloc[:,-1])) #Take just the first (geneid) attribute from the last column
    
    transcripts, exons, genes = {}, {}, {}
    for n in filter_gtf.iloc[:,-1:].iterrows():
        index = n[0]
        for att in n[1].iloc[0].split(sep=';'):
            if "transcript_id" in att:
                transcripts[index] = att
            elif "exon_number" in att:
                exons[index] = att
            elif "gene_id" in att:
                genes[index] = att
    exon_series = pd.Series(exons)
    transcripts = pd.Series(transcripts)
    gene_ids = pd.Series(genes)
                
    annot_gtf = pd.concat([filter_gtf.iloc[:,:-1], transcripts, exon_series, gene_ids], axis=1,) #remove last column and add relevant attributes as additional columns
    
    no_dups = annot_gtf.drop_duplicates(subset=['start','end'], keep='first') #remove rows with duplicate gene_ids
    
    sorts = no_dups.sort_values(by=['start'])

    overlap = 0

    last = 0
    for row in no_dups.loc[:,'start':'end'].iterrows():
        #print(row[1]['end'])
        this = row[1]['start']
        if this < last:
            overlap +=1
        last = row[1]['end']
    print(overlap)
    
    #print(genes.iloc[:15,3:])
    print (filter_gtf.shape, no_dups.shape)
    '''
    bp = 0
    for row in gtf.loc[:,'start':'end'].iterrows(): #iterate over just the 'start' and 'end' columns
        start = row[1].iloc[0]
        end = row[1].iloc[1]
        bp += end - start + 1
    print(gtf_file, bp)
    return bp  

if __name__ == '__main__':
    fasta = "../lace04/superT/demo_SuperDuper.fa"
    real = "/home/sarah/packages/necklace/demo_data/data/Ovis_aries.Oar_v3.1.90.chr14.gtf"
    flat = "sheep.flat.gtf"
    bp_in_fasta (fasta)
    bp_in_gtf (flat)
    bp_in_gtf (real)
