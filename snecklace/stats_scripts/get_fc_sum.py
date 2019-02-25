"""Merge feature counts summary file from all samples into one.
   - Assigned
   - Unassigned_Unmapped
   - Unassigned_MultiMapping
   - Unassigned_NoFeatures
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

SUM_SUFFIX = ".summary"

def _getSamples(directory="hisat.out"):
    names = [n for n in os.listdir(directory) if n.endswith(SUM_SUFFIX)]
    return names

def __getValue(line):
    result = line.split("(")[-1]
    result = result.split(")")[0]
    return result

def _getLineAverage(line):
    nums = line.strip().split()[1:]
    for i in range(len(nums)):
        nums[i] = int(nums[i])
    average = round ( sum(nums) / len(nums) )
    return average

def getFeatureSummary(datadir="counts/",outpath="fc_sum.tab"):
    samples = _getSamples(datadir)
    columns = ["sample", "Assigned","Unassigned_Unmapped",
               "Unassigned_MultiMapping", "Unassigned_NoFeatures"]
    collate = []
    for sample in samples:
        sampleID = sample[:13]
        path = os.path.join(datadir, sample)
        assigned, amb, unamb = 0, 0, 0
        f = open(path, 'r')
        for line in f:
            if line.startswith("Assigned"):
                assigned = _getLineAverage(line)
            elif line.startswith("Unassigned_Unmapped"):
                unmap =  _getLineAverage(line)
            elif line.startswith("Unassigned_MultiMapping"):
                multi =  _getLineAverage(line)
            elif line.startswith ("Unassigned_NoFeatures"):
                unamb =  _getLineAverage(line)
        f.close()
        collate.append([sampleID, assigned, unmap, multi,unamb])
    result = pandas.DataFrame(collate, columns=columns)
    result.to_csv(outpath, sep='\t', index=False)
    return result

if __name__ == '__main__':
    directory = '../stat-test01/counts_stats'
    outdir = "fc_sum.tab"
    getFeatureSummary(datadir=directory, outpath=outdir)