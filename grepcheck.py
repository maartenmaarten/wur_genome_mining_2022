
'''
12-10-22 MPBoneschansker

check whether each file contains id's contained in a master file.
Needed to check for clusters containing only enrichment sequences.

'''

from Bio import SeqIO
import sys

master_fasta, check_fasta = sys.argv[1], sys.argv[2]
master_id = [] # list of ids in master file
count = 0

# generate master id list
for seq_record in SeqIO.parse(master_fasta, "fasta"):
	master_id.append(seq_record.id)
	

for seq_record in SeqIO.parse(check_fasta, "fasta"):
	if seq_record.id in master_id:

		count += 1

print(master_fasta)
print(count)

