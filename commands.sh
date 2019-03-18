#!/usr/bin/env bash

#cd /home/output_data/workflows
<<<<<<< HEAD
source activate nlace3 #activate conda env
DIR=".." #set wd

#necklace test case
#use -n for dryrun; use just -pr for a real run
snakemake -s snecklace/Snakefile -d $DIR --configfile sheep-demo.json --cores 28  --use-conda -npr --prioritize de_novo_assembly #> test_run.log 2>&1 &  #to log the progress of the pipeline (captures errors)
#tail -f test_run.log

#test blat/pblat (after creating genome superT and denovo assembly):
#snakemake -s snecklace/Snakefile -d $DIR --configfile 'sheep-demo.json' --cores 28 --use-conda -pr blat_genomeST_denovo
=======
source activate nlace3
DIR="/home/sarah/projects/talens_mouse/pooled_testis_brain_rspermatids/necklace/tmp"

#necklace test case
snakemake -s snecklace/Snakefile -d $DIR --configfile 'test.config.json' -j 28  --use-conda -npr --prioritize de_novo_assembly #> test_run.log 2>&1 &
#tail -f test_run.log

#test blat/pblat:
#snakemake -s snecklace/Snakefile -d $DIR --configfile 'test.config.json' -j 28 --use-conda -pr blat_genomeST_denovo
>>>>>>> 2b109e055d84f83a06b75a8d6460540877eeec73

#conda test
#conda create -f snecklace/envs/lace.yml --name lace

<<<<<<< HEAD
#test lace independently (after creating cluster files):
#snakemake -s snecklace/Snakefile -d /home --configfile 'sheep-demo.json' --cores 28 --use-conda -pr run_lace --force

#Example of cluster set up
#snakemake --cluster-config cluster.json \
 #  --cluster "qsub -V -b y -pe threads {threads} \
  # -l h_vmem={cluster.h_vmem},virtual_free={cluster.virtual_free} \
 #  -q {cluster.queue} \
#   -o {cluster.stdout_dir} -e {cluster.errout_dir}" -j 100 \
  # -s snecklace/Snakefile -d $DIR \
   #--configfile sheep-demo.json \
    #-use-conda -pr --prioritize de_novo_assembly > run1.log 2>&1 &
#ail -f run1.log
=======
#symlink test
#ln -s config.json master.config.json

#test lace independently:
#snakemake -s snecklace/Snakefile -d /home --configfile 'test.config.json' --cores --use-conda -pr run_lace --force
>>>>>>> 2b109e055d84f83a06b75a8d6460540877eeec73
