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



logger = logging.getLogger("grab_and_link.py")
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='List RefSeq .fasta files from input folder.', usage="grab_and_link.py ../Norovirus_and_Sapovirus/Nucleotide/")

parser.add_argument('dir', type=readable_dir, action='store')

parser.add_argument('--seqid2taxid', default='../centrifuge/seqid2taxid.map')

args = parser.parse_args()

inFolder = args.dir

#table = args.seqid2taxid

seqid2taxid = {}

with open(args.seqid2taxid, "r") as table:
        tsv_reader = csv.reader(table, delimiter=";")
        for row in tsv_reader:
                 splitRow = re.split(r'\s+', row[0])
                 seqid2taxid[splitRow[0]] = splitRow[1]


origWD = os.getcwd()

#print("{}/{}".format(origWD, inFolder))

nuclFolder = re.sub(r'\.\.', '', inFolder)

parent = getParentDir(origWD)

#print(parent)

getFasta = os.listdir(inFolder)

### Final loop to output a CreateTaxDB comma-delimited sample file

print("id,taxid,fasta_dna,fasta_aa")

for f in getFasta:
        acc = re.sub(r'\.fasta', '', f)
        prot = re.sub(r'fasta', 'faa', f)
        protFolder = re.sub(r'Nucleotide', 'Protein', nuclFolder)
        print("{},{},{}{}{},{}{}{}".format(acc.strip(), seqid2taxid[acc.strip()], parent, nuclFolder, f, parent, protFolder, prot))

