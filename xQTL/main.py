#!/usr/bin/env python3

"""
Tool to simulate expression data

Example command:
xQTL-run --input test/sim-0/matrixEQTL.out --out test
"""

import argparse
import numpy as np
import os
import pandas as pd
from scipy import stats
import sys

from xQTL import __version__

def ERROR(msg):
	sys.stderr.write("[ERROR]: " + msg.strip() + "\n")
	sys.exit(1)

def MSG(msg):
	sys.stderr.write("[PROGRESS]: " + msg.strip() + "\n")

def main(args):
	if not os.path.exists(args.input):
		ERROR("Could not find %s"%args.input)

	# Load Matrix eQTL data
	data = pd.read_csv(args.input, sep="\t")
	#zscores = data.pivot_table(index='SNP', columns='gene', values='t-stat')

	# Convert tvals to pvals
	#print(zscores) # TODO figure this out
	#pvalues = 2*stats.norm.cdf(-np.abs(zscores))
	#print(pvalues)
	#zscores["pval"] = 2*stats.norm.cdf(-np.abs(zscores))

	# TODO - compute test statistics, either 
	# using CPMA  ./calculate_cpma.py
	# or xQTL ./calculate_mixturemodel.py
	# Add options for either

	# TODO - get pval on test stat

	ERROR("Not implemented")

def getargs(): 
    parser = argparse.ArgumentParser(__doc__)
    run_group = parser.add_argument_group("xQTL run parameters")
    run_group.add_argument("-s", "--seed", help="Seed for random generator", type=int, default=0, )
    inout_group = parser.add_argument_group("Input/output")
    inout_group.add_argument("--input", help="Matrix eQTL file", type=str, required=True)
    inout_group.add_argument("--out", help="Output prefix", type=str, required=True)
    ver_group = parser.add_argument_group("Version")
    ver_group.add_argument("--version", action="version", version = '{version}'.format(version=__version__))
    args = parser.parse_args()
    return args

def run():
    args = getargs()
    if args == None:
        sys.exit(1)
    else:
        retcode = main(args)
        sys.exit(retcode)

if __name__ == "__main__":
    run()