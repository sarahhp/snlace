#!/usr/bin/env bash

cd /home/nlaceoutput/workflows
#pre-trim dryrun
#snakemake -s trim_subsample.py -d ../ --configfile config.json --cores 1 -npr 
#necklace dryrun
#snakemake -s snecklace/Snakefile -d ../ --configfile config.json --cores 1 --use-conda -npr

#trim datasets: testes, brain and round spermatids. 
#In reality the brain and spermatid filenames were changed from the raw files as a 
#part of trimming and preprocessing
#snakemake -s trim_subsample.py -d ../ --configfile trim1.config.json --cores 40 -pr
#snakemake -s trim_subsample.py -d ../ --configfile trim2.config.json --cores 40 -pr
#snakemake -s trim_subsample.py -d ../ --configfile trim3.config.json --cores 40 -pr



#necklace test case
snakemake -s snecklace/Snakefile -d ../ --configfile 'test.config.json' --cores 40 --use-conda -pr

#conda test
#conda create -f snecklace/envs/lace.yml --name lace

#symlink test
#ln -s config.json master.config.json 
