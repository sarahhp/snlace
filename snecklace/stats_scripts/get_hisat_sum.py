"""
Merge key statistics from hisat summaries into one file
    - no. reads
    - alignment rate (%)
    - UniqueCon rate (%)
    - Unique non-Con rate(%)
    - Multimapping rate (%) 
"""
__author__ = "Created by Hua Ying, modified by Sarah Hazell Pickering"
__date__ = "2018-09-27"

import os
import numpy
import pandas
pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 200)
import Bio.Seq

SUM_SUFFIX = ".sum.txt"

def _getSamples(directory="hisat.out"):
    names = [n for n in os.listdir(directory) if n.endswith(SUM_SUFFIX)]
    return names

def __getValue(line):
    result = line.split("(")[-1]
    result = result.split(")")[0]
    return result

def __calcTotalPercent(pairs, singles, reads):
    number = ( (pairs*2 + singles) / (reads*2) )*100
    percentage = str( round(number, 2) ) + "%"
    return percentage

def getAverages(collate):
    sums = [0,0,0,0,0]
    for line in collate:
        sample, reads, overall, uniqueCon, unique_nonCon, multi = line
        sums[0] += reads
        sums[1] += float(overall[:-1])
        sums[2] += float(uniqueCon[:-1])
        sums[3] += float(unique_nonCon[:-1])
        sums[4] += float(multi[:-1])
    try:
        averages = [str (round (n/(len (collate) ),2 ) ) + "%" for n in sums]
    except ZeroDivisionError as error:
        print("Found ZeroDivisionError at line 46 of getAverages. This may \
              mean that there are no matching files in the directory supplied, \
              or the matching files have an unexpected format")
    averages[0] = averages[0][:-1] #removing '%' from read total stat
    final_line = ["Averages"] + averages
    return final_line

def getHisatSummary(datadir="mapped_reads", outpath="hisat_summary.tab"):
    samples = _getSamples(datadir)
    columns = ["sample", "total reads", "% overall mapped", "% UniqueCon",
               "% Unique non-Con", "% multiply mapped"]#
    collate = []
    for sample in samples:
        print (sample)
        path = os.path.join(datadir, sample)
        f = open(path, 'r')
        for line in f:
            line = line.strip()
            if line.endswith("reads; of these:"):
                reads = int(line.split()[0])
            elif line.endswith("overall alignment rate"):
                overall = line.split()[0]
            elif line.endswith("aligned concordantly exactly 1 time"):
                uniqueCon = __getValue(line)
            elif line.endswith("aligned discordantly 1 time"):
                uniqueDis = int(line.split()[0])
            elif line.endswith("aligned exactly 1 time"):
                unique_nonConDis = int(line.split()[0])
            elif line.endswith("aligned concordantly >1 times"):
                multiCon = int(line.split()[0])
            elif line.endswith("aligned >1 times"):
                multi_nonCon = int(line.split()[0])
        f.close()

        sampleID = sample.replace(SUM_SUFFIX, '')
        unique_nonCon = __calcTotalPercent(uniqueDis, unique_nonConDis, reads) 
        multi = __calcTotalPercent(multiCon, multi_nonCon, reads)  

        collate.append([sampleID, reads, overall, uniqueCon, unique_nonCon, multi]) #unique_dis, unique_noPE, multi_noPE])
    averages = getAverages(collate)
    collate.append(averages)
    result = pandas.DataFrame(collate, columns=columns)
    result.to_csv(outpath, sep='\t', index=False)
    return averages

def extractAverages(summary="hisat_summary.tab"):
    averages = pandas.read_table(summary).iloc[-1,1:] #select last row of summary file
    return averages
    

if __name__ == '__main__':
    data = "../map-test02/mapped_reads/"
    outdir = "hisat_summary.tab"
    getHisatSummary(datadir=data, outpath=outdir)
    extractAverages(summary=outdir)
