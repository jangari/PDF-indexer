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
    v_sort=v # For single pages, v_sort is simply v.

    pattern = re.compile("(.*)\s+\(([0-9]+-[0-9]+)\)")
    if re.match(pattern,k):
        match = pattern.search(k)
        k = match.group(1)
        v = match.group(2)
        vp = re.compile("([0-9]+)-") # Parse the start number of the page range to be the sort value
        vm = vp.search(v)
        v_sort = int(vm.group(1))
    if index.has_key(k): # Don't duplicate entries
        if not (v_sort,v) in index[k]:
            index[k].append((v_sort,v)) # Don't duplicate pages
    else:
        index[k]=[(v_sort,v)] # Add dict entry if not already present

for k in sorted(index, key=lambda s: s.lower()): # Sort dict by key
    index[k].sort() # Sort each value list numerically
    vlist = []
    for vtuple in index[k]: # Pull page refs out of tuples and create list
        vlist.append(vtuple[1])
    print k+'\t'+', '.join(map(str, vlist)) # Print the list of page refs
