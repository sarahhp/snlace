# snlace

"Necklace" pipeline for creation of custom transcriptomes from RNAseq datasets, implemented in snakemake.  Pipeline first published by Davidson et al. 2017 in Genome Biology.  Tools used by the pipeline not included.  I reccommend to use this either with the corresponding dockerfile: https://hub.docker.com/r/sarahhp/snlace/, or in another type of virtual environment (e.g. conda).  

Pipeline consists of two snakemake workflows.  One for preprocessing of the raw data (quality control, trimming and optional subsetting) stored in the trim_subsample.py file.  The second runs the full necklace pipeline on processed data (snecklace/Snakefile), including some final summary statistics.  If preprocessing is not required only run the second snakemake command in the commands.sh file. 

Quick install and run on a demo dataset:

Clone this repository (not necessary if using the docker image)
```
git clone https://github.com/sarahhp/snlace.git
cd snlace
```

Create a conda environment with the necessary packages (not necessary if using the docker image)
```
conda env create -f snecklace/envs/nlace.yml --name nlace
source activate nlace
```

Download demo data
```
wget https://github.com/Oshlack/necklace/wiki/asserts/sheep_small_demo_data.tar.gz
tar -C ../data -zxvf sheep_small_demo_data.tar.gz
```

Install extra tools (not necessary if using the docker image)
```
g++ -o tools/cluster tools/cluster.c
g++ -o tools/gtf2flatgtf tools/gtf2flatgtf.c
g++ -o tools/make_blocks tools/make_blocks.c
```

Download pblat from http://icebert.github.io/pblat/ and run `make` in the main dir. 

Dryrun:
`bash commands.sh` OR `snakemake -s snecklace/Snakefile -d .. --configfile sheep-demo.json --use-conda -npr`

To run, remove -n option from uncommented line in commands.sh OR run  `snakemake -s snecklace/Snakefile -d .. --configfile sheep-demo.json --use-conda -pr`

See Also:
- https://conda.io/en/latest/
- https://snakemake.readthedocs.io/en/stable/
- https://github.com/Oshlack/necklace

Usage:
1. Set up an environment with the following tools and their dependencies:
  for both workflows: 
  - snakemake (at least 3.4 (I think) for snecklace pipeline) 

  for preprocessing workflow only: 
  - fastp 
  - seqtk
  - gzip

  for snecklace: 
  - hisat2 
  - samtools 
  - stringtie 
  - gffread 
  - trinity 
  - blat 
  - subread 
  - biopython 
  - pandas

2. Edit the config.json file with paths to data and reference genomes.  To line 34 of the snecklace/scripts/get_stats.py you may have to add the absolute path of the snecklace/stats_scripts.  This is because the python scripts used by get_stats are not globally installed and their location must be appended to the python path.   

3. Run the pipeline by executing the commands.sh file (bash /home/commands.sh) or by running the contained snakemakemake commands directly on the CLI.  -n allows a dryrun of the pipeline.  


