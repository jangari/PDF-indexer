#!/usr/local/bin/python

# Written by Aidan Wilson on 2017-09-04.

# Generates tab-delimited text formatted for a book index, with reference and # a list of page
# numbers. Input is a tab-delimited file that has been outp# ut from a pdf containing page
# references and annotations. The expectation is that the user will undertake post-processing work
# with the generated text, such as separate alphabetic blocks, add 'see x' references and create
# subcategories (currently not supported here).

# Limitations
#
# Page ranges should be entered into the comment text in the pdf, and the actual page
# where it is entered is overwritten, rendering it meaningless. Also, as page ranges (such as 95-98)
# cannot be coerced into an integer, they cannot be sorted within the list of page references. In
# a future version, each list entry could be a tuple, with a sort key, often the same as the page
# number, but for ranges, will be filled by the integer of the first part of the range.
#
# [(11,'11'),(95,'95-98')]

# The entire index is a dictionary, with the referenced text being the keys, and
# a list of page numbers (stored as strings) being the value.
# TODO: Support for subcategories of indexes, e.g.:

# LDS
#    -History     10-17
#    -Culture     14, 16, 19
#    -People      61-76

# Currently this is only supported through manual means, by, for example, manually entering
# the top-level category in each pdf annotation with consistent means. For the above example,
# the pdf annotations could be "LDS | History", "LDS | Culture", etc. Post-processing would be
# needed to then convert this into a top-level category and subcategories.

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
    if index.has_key(k):
        if not v in index[k]:
            index[k].append(v)
    else:
        index[k]=[v]

for k in sorted(index):
    index[k].sort()
    print k+'\t'+', '.join(map(str, index[k]))
