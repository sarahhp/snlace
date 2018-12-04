# snlace

"Necklace" pipeline for creation of custom transcriptomes from RNAseq datasets, implemented in snakemake.  Pipeline first published by Davidson and Ohslack 2017.  Tools used by the pipeline not included.  I reccommend to use this either with the corresponding dockerfile: https://hub.docker.com/r/sarahhp/snlace/, or in another type of virtual environment (e.g. conda).  

Pipeline consists of two snakemake workflows.  One for preprocessing of the raw data (quality control, trimming and optional subsetting) stored in the trim_subsample.py file.  The second runs the full necklace pipeline on processed data (snecklace/Snakefile), including some final summary statistics.  If preprocessing is not required only run the second snakemake command in the commands.sh file. 

To run:

1. Set up an enviornment with the following tools and their dependencies:
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

2. Edit the config.json file with paths to data and reference genomes.  

3. Run the pipeline by executing the commands.sh file (bash /home/commands.sh) or by running the contained snakemakemake commands directly on the CLI.  -n allows a dryrun of the pipeline.  


