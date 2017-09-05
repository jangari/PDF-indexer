#!/usr/local/bin/python

import re, sys

index={}

input_file=sys.argv[1] # Load file from argument
comments_file=open(input_file,'r')

for line in comments_file:
    v,k = line.split('\t') # Split index reference into page ref and text
    k=k.rstrip() # Strip any whitespace
    v=int(v)-8

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
