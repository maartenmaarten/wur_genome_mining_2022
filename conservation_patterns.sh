#!/bin/bash

'''
author: MP Boneschansker, 21-12-22
This script takes in a fasta and outputs a normalized conservation score per
residue. 

command line arguments needed $FASTA_FILE 

$1 input file.fasta
$2 project name

optional 
enrichment: enrich data with homologs from specified database for more
meaningful alignment
jalview: generate and show plots of alignment, not recommended for large datasets
precursor_plot: generate precursor plot with python precursor_plot2.py script

'''

# CONFIGS
enrich=true
jalview=true
precursor_plot=true
database='/lustre/BIF/nobackup/bones005/databases/200aa_nr.dmnd'
ripp=0

# exit bash if ANY command fails
set -e
trap echo "\"${last_command}\" command filed with exit code $?." EXIT

# check if programs are there

# clean up fasta record names
cat $1 | tr '\*' ' ' > $2'.fasta'

# split fastas per sequence
mkdir -p 'split_fastas'
python ../fasta_split.py $2'.fasta'

# enrich module, runs a blast search agains db and efetches sequences
if $enrich
then
test ! -f $database && {echo 'database file does not exsist' ; exit 1}
echo 'database used for enrichment is '$database
for i in split_fastas/*.fasta
do
cat $i > ${i:0:-6}'_enriched.fasta'
echo running diamond on $i
time diamond blastp -q $i -d $database -o $i'_dmnd_results' \
--quiet --fast --no-self-hits -t ../../../../../../dev/shm/
# note that this uniq is not uniq for sequence but for id + seq
awk '$3 != 100 && $3 > 50 {print $2}' $i'_dmnd_results' | sort | uniq | \
efetch -db protein -format fasta >> ${i:0:-6}'_enriched.fasta'
done
fi

# if enriched fastas contain less than 5 seqs, delete
mkdir -p split_fastas/too_small/
for i in split_fastas/*_enriched.fasta; do if (( $(grep -c '>' $i) < 5 )); then echo 'too small' && \
mv $i split_fastas/too_small/; else echo 'right size!'; fi; done

# run muscle on each fasta
mkdir -p afas
for i in split_fastas/*enriched.fasta; 
do muscle -align $i -output afas/${i:12:-6}.afa &&\
trimal -nogaps -in afas/${i:12:-6}.afa -out afas/${i:12:-6}'_trimmed.afa' 
done


# run aacon on each afa
mkdir -p aacon
for i in afas/*trimmed.afa; do java -jar ../compbio-conservation-1.1.jar -i=$i -n -o=aacon/${i:5:-12}'_aacon'; done

# optionally create jalview figures of alignment afa
if $jalview
then 
mkdir -p jalviews
for i in afas/*trimmed.afa; do java -jar ../jalview-all-2.11.2.2-j1.8.jar \
-headless -colour taylor -open $i -png $i.png -setprop SORT_ALIGNMENT='Percentage Identity'
done
fi
mv afas/*.png jalviews

# optionally create precursor conservation graphs
if $precursor_plot
then
mkdir -p precursor_plots
for i in aacon/*aacon; do python ../precursor_plot2.py $i
done
fi

mv aacon/*.png precursor_plots

# run pre_process_aacon.py folder, is it ripp or not, project name
python3 pre_process_aacon.py aacon/ $ripp $2



exit 0



