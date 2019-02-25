#!/usr/bin/env bash

#cd /home/output_data/workflows
source activate nlace3
DIR="/home/sarah/projects/talens_mouse/pooled_testis_brain_rspermatids/necklace/tmp"

#necklace test case
snakemake -s snecklace/Snakefile -d $DIR --configfile 'test.config.json' -j 28  --use-conda -npr --prioritize de_novo_assembly > test_run.log 2>&1 &
#tail -f test_run.log

#test blat/pblat:
#snakemake -s snecklace/Snakefile -d $DIR --configfile 'test.config.json' -j 28 --use-conda -pr blat_genomeST_denovo

#conda test
#conda create -f snecklace/envs/lace.yml --name lace

#symlink test
#ln -s config.json master.config.json

#test lace independently:
#snakemake -s snecklace/Snakefile -d /home --configfile 'test.config.json' --cores --use-conda -pr run_lace --force
