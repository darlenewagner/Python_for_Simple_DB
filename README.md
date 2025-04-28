## Python VE Scripts for Creating Nucleotide and Protein Sequence Databases.

### Installation:

`module load python/3.12.3`

`virtualenv -p /apps/x86_64/Python/3.12.3-GCCcore-13.3.0/bin/python3 Python_for_Simple_DB/`

`cd Python_for_Simple_DB/`

`bin/pip install biopython`

`mkdir convert`

`python3 -m pip install seqconverter --target convert/`

`python3 -m pip install pandas --target convert/`

### Running with multiple Genbank file input plus nucleotide .fasta and protein .faa output

`bin/python3 genbank_convert.py ../Rotavirus/Genbank/ ../Rotavirus/Nucleotide/ --outdir2 ../Rotavirus/Protein/`
