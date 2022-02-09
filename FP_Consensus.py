#!/usr/bin/env python

from Bio import SeqIO
import argparse

def get_args(): # generalize code using argparse
    parser = argparse.ArgumentParser(description="A program to input sanger reads")
    parser.add_argument("-f", help="FWD_ab1", required=True, type=str)
    return parser.parse_args()
     
args = get_args()

f = args.f

# Convert ab1 to fasta:

# open a fastq to write to:
FP_Consensus_fastq = open("FP_Consensus.fastq", "a")

record = SeqIO.parse(f, "abi") # reads the ab1 file
count = SeqIO.write(record, FP_Consensus_fastq, "fastq") # converts to fastq and writes it to the FP_Consensus_fastq file

FP_Consensus_fastq.close() # close the file

