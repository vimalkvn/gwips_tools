#!/bin/bash
# This script must be run with sudo
GENOMES="hg19 mm10 danRer7 dm3 ce10 sacCer3"

cd /home/vimal/Workspace/gwips_tools
python gwips_tools/update_annotations.py -a

for genome in $GENOMES
do
    python gwips_tools/update_refseq.py -g $genome
done

service mysql reload