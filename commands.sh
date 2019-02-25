#!/usr/bin/env bash

#cd /home/output_data/workflows
source activate nlace3
DIR="/home/sarah/projects/talens_mouse/pooled_testis_brain_rspermatids/necklace/tmp"

#pre-trim dryrun
#nakemake -s trim_subsample.py -d /home --configfile config.json --cores 1 -npr 
#necklace dryrun
#snakemake -s snecklace/Snakefile -d $DIR --configfile config.json --cores 1 --use-conda -npr

#trim datasets: testes, brain and round spermatids. 
#In reality the brain and spermatid filenames were changed from the raw files as a 
#part of trimming and preprocessing
#snakemake -s trim_subsample.py -d /home --configfile config.json --cores 40 -pr

#necklace test case
#snakemake -s snecklace/Snakefile -d $DIR --configfile 'test.config.json' -j 28  --use-conda -pr --prioritize de_novo_assembly > test_run.log 2>&1 &
#tail -f test_run.log
#snakemake -s snecklace/Snakefile -d /home --configfile 'test.config.json' -j 8 --use-conda -pr --force count_reads
#snakemake -s snecklace/Snakefile -d /home --configfile 'test.config.json' -j 4 --use-conda -pr --force count_reads
#snakemake -s snecklace/Snakefile -d /home --configfile 'test.config.json' -j 2 --use-conda -pr --force count_reads

#test blat/pblat:
#snakemake -s snecklace/Snakefile -d $DIR --configfile 'test.config.json' -j 28 --use-conda -pr blat_genomeST_denovo

#conda test
#conda create -f snecklace/envs/lace.yml --name lace

#symlink test
#ln -s config.json master.config.json

#test lace independently:
#nakemake -s snecklace/Snakefile -d /home --configfile 'test.config.json' --cores --use-conda -pr run_lace --force

FULL="/home/sarah/projects/talens_mouse/pooled_testis_brain_rspermatids/necklace/all"
#-------------FULL RUN ----------------------------
#snakemake -s snecklace/Snakefile -d $FULL --configfile config.json -j 32  --use-conda -npr --prioritize de_novo_assembly 
#snakemake -s snecklace/Snakefile -d $FULL --configfile config.json -j 32  --use-conda -pr --prioritize de_novo_assembly > run4.log 2>&1 &
snakemake -s snecklace/Snakefile -d $FULL --configfile config.json -j 31 --use-conda -pr > run10.log 2>&1 &
#nakemake -s snecklace/Snakefile -d $FULL --configfile config.json -j 32 --use-conda -pr --resources mem_mb=100 
#python /home/sarah/projects/talens_mouse/pooled_testis_brain_rspermatids/necklace/all/.snakemake/conda/019ee3c9/bin/Lace.py \
#--cores 31 --maxTran 40 --outputDir $FULL/superT/SuperFiles $FULL/clustering/talens_sequences.fa \
#$FULL/clustering/talens.clusters > run10.log 2>&1 &
tail -f run10.log
