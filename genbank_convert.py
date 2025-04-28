#!/usr/bin/python

import sys
import os.path
import argparse
import re
import logging
import warnings
import subprocess
import csv
from os import listdir
from os.path import isfile, join

### Generates nucleotide .fasta and (multi)fasta-formatted amino acid files from GenBank-formatted input ###
### Input folder required and Output1 folder required.  Output2 folder optional.
### Requires Biopython and installation of seqconverter.py ###

from Bio import SeqIO

### Does not require pandas ###

def readable_dir(prospective_dir):
        if not os.path.isdir(prospective_dir):
                raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
                if( not prospective_dir.endswith("/") ):
                        prospective_dir = prospective_dir + "/"
                return prospective_dir
        else:
                raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


def getParentDir(filePathString):
        splitStr = re.split(pattern='/', string=filePathString)
        folderCount = len(splitStr) - 1
        isolatePath=splitStr[0]
        ii = 1
        while ii < folderCount:
                isolatePath = isolatePath + "/" + splitStr[ii]
                ii = ii + 1
        return isolatePath

logger = logging.getLogger("genbank_convert.py")
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='List RefSeq .gbk files from input folder.', usage="genbank_convert.py ../Rotavirus/Genbank/")

parser.add_argument('indir', type=readable_dir, action='store')

parser.add_argument('outdir1', type=readable_dir, action='store')

parser.add_argument('--outdir2', type=readable_dir, action='store')

parser.add_argument('--seqid2taxid', default='../centrifuge/seqid2taxid.map')

args = parser.parse_args()

inFolder = args.indir

origWD = os.getcwd()

outNucl = origWD + "/temp_output/dna.fasta"

#print("{}/{}".format(origWD, inFolder))

gbkFolder = re.sub(r'\.\.', '', inFolder)

parent = getParentDir(origWD)

getGBK = os.listdir(parent + gbkFolder)

myPath = parent + gbkFolder + getGBK[0]

os.system("python convert/seqconverter.py --informat genbank -i {} > {}".format(inFolder+getGBK[0], outNucl))

input_handle = open(myPath, 'r+')

#print(input_handle)

protCoords = []

for line in input_handle:
        if(re.search(r'CDS', line)):
                temp = line.split()
                protCoords.append(temp[1])

coordinates = protCoords[0].split('..')

with open(outNucl, "r") as fasHandle, open("./temp_output/cds.fasta", "w") as output_handle:
        for record in SeqIO.parse(fasHandle, "fasta"):
            trimmed_seq = record.seq[int(coordinates[0])-1:int(coordinates[1])]
            record.seq = trimmed_seq
            SeqIO.write(record, output_handle, "fasta")


cleanGBK = re.sub(r'\.gbk', '', getGBK[0])
            
if(args.outdir2 is not None):
        os.system("python convert/seqconverter.py --informat genbank -i {} > {}{}".format(inFolder+getGBK[0], args.outdir1, cleanGBK+'.fasta'))
        os.system("python convert/seqconverter.py --informat fasta --translate 1 -i {} > {}{}".format("./temp_output/cds.fasta", args.outdir2, cleanGBK+'.faa'))
else:
        os.system("python convert/seqconverter.py --informat genbank -i {} > {}{}".format(inFolder+getGBK[0], args.outdir1, cleanGBK+'.fasta'))


