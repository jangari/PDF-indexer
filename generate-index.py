#!/usr/local/bin/python

import re, sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("-o", "--offset", type=int, help="Set frontmatter offset", dest="OFFSET", default=0)
args = parser.parse_args()

index={}
comments_file=open(args.input_file,'r')
OFFSET=args.OFFSET

for line in comments_file:
    v,k = line.split('\t') # Split index reference into page ref and text
    k=k.rstrip() # Strip any whitespace
    v=int(v)-OFFSET

    pattern = re.compile("(.*)\s+\(([0-9]+-[0-9]+)\)")
    if re.match(pattern,k):
        match = pattern.search(k)
        k = match.group(1)
        v = match.group(2)
    if index.has_key(k): # Don't duplicate entries
        if not v in index[k]:
            index[k].append(v) # Don't duplicate pages
    else:
        index[k]=[v] # Add dict entry if not already present

for k in sorted(index): # Sort dict by key
    index[k].sort() # Sort each value list numerically
    print k+'\t'+', '.join(map(str, index[k]))
