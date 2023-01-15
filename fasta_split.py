from Bio import SeqIO
import sys

input_file = sys.argv[1]

for seq_record in SeqIO.parse(input_file, "fasta"):
	SeqIO.write(seq_record, 'split_fastas/'+\
	str(seq_record.id).replace("/",'|')[:50]+'.fasta', "fasta") # add regex/pythonic split
	
