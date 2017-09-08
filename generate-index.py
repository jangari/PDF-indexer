#!/usr/bin/python

import re, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--offset", type=int, help="Set frontmatter offset for page numbers to be correctly rendered.", dest="OFFSET", default=0)
parser.add_argument("-s", "--separator", type=str, help="Set output field separator between index entry and locator. Default is a tab character.", default="\t", dest="separator")
parser.add_argument("-g", "--group", action="store_true", help="Display output entries in alphabetic groups separated by line breaks and section headings.")
parser.add_argument("-w", "--word-sort", action="store_true", help="Sorts entries using word-by-word alphabetic order (de Marco > dean).", default=False, dest="word")
parser.add_argument("-l", "--letter-sort", action="store_true", help="Sorts entries using letter-by-letter alphabetic order (dean > de Marco). True by default.", default=True, dest="letter")
parser.add_argument("-e", "--elide", action="store_true", help="Elide numbers in page ranges where possible (excluding teens).", dest="elide")
parser.add_argument("input_file")
args = parser.parse_args()

def elide(start,end):
    elide=0
    if len(start) == len(end):
        for i in range(0,len(start)):
            if start[i] == end[i]:
                if i == len(start)-2 and end[-2] == "1":
                    continue
                else:
                    elide=i+1
            else:
                break
    return start, end[elide:]

index={}
comments_file=open(args.input_file,'r')
OFFSET=args.OFFSET

for line in comments_file:
    v,k = line.split('\t') # Split index reference into page ref and text
    k = k.rstrip() # Strip any whitespace
    v = int(v)-OFFSET
    v_sort = v # For single pages, v_sort is simply v.

    pattern = re.compile("(.*)\s+\(([0-9]+(n[0-9]+|\-[0-9]+))\)")
    if re.match(pattern,k):
        match = pattern.search(k)
        k = match.group(1)
        v = match.group(2)
        vp = re.compile("([0-9]+)(-|n)") # Parse the start number of the page range to be the sort value
        vm = vp.search(v)
        v_sort = int(vm.group(1))

        if args.elide and '-' in v:
            vstart, vend = v.split('-')
            vstart, vend = elide(vstart,vend)
            v = vstart+"-"+vend

    if k in index: # Don't duplicate entries
        if not (v_sort,v) in index[k]:
            index[k].append((v_sort,v)) # Don't duplicate pages
    else:
        index[k] = [(v_sort,v)] # Add dict entry if not already present

k_prev=None

if args.word:
    index_sorted = sorted(index, key=lambda s: s.lower())
else:
    index_sorted = sorted(index, key=lambda s: s.replace(',','').replace(' ','').lower())

for k in index_sorted:
    k_this=k[0].upper()
    index[k].sort() # Sort each value list numerically
    vlist = []
    for vtuple in index[k]: # Pull page refs out of tuples and create list
        vlist.append(vtuple[1])
    if args.group:
        if k_this != k_prev:
            k_prev = k_this
            print('\n'+k_this)
    print(k+args.separator+', '.join(map(str, vlist))) # Print the list of page refs

#TODO: Use this function to allow for subheadings:
# def output(d,sep=""):
#     for k in sorted(d):
#         if type(d[k]) != dict:
#             vlist=[]
#             for vtuple in d[k]:
#                 vlist.append(vtuple[1])
#             print(sep+k+"\t"+','.join(map(str,vlist)))
#         else:
#             print(k)
#             output(d[k],sep=" – ")
#
# And this for entering subheading data into the dict cleanly:
# import re
# index={}
# comments_file = open('input','r')
# for line in comments_file:
#     v,k = line.split('\t') # Split index reference into page ref and text
#     k = k.rstrip() # Strip any whitespace
#     v = int(v)
#     v_sort = v # For single pages, v_sort is simply v.
#
#     pattern = re.compile("(.*)\s+\(([0-9]+(n[0-9]+|\-[0-9]+))\)")
#     if re.match(pattern,k):
#         match = pattern.search(k)
#         k = match.group(1)
#         v = match.group(2)
#         vp = re.compile("([0-9]+)(-|n)") # Parse the start number of the page range to be the sort value
#         vm = vp.search(v)
#         v_sort = int(vm.group(1))
#
#     sh_pattern=re.compile("(.*?)\s\|\s(.*)")
#     if re.match(sh_pattern,k):
#         sh_match=sh_pattern.search(k)
#         k = sh_match.group(1).rstrip().lstrip()
#         sh = sh_match.group(2).rstrip().lstrip()
#         if k in index:
#             if sh in index[k]:
#                 if not (v_sort,v) in index[k][sh]:
#                     index[k][sh]=[(v_sort,v)]
#             else:
#                 index[k][sh]=[(v_sort,v)]
#         else:
#             index[k]={sh:[(v_sort,v)]}
#     else:
#         if k in index: # Don't duplicate entries
#             if not (v_sort,v) in index[k]:
#                 index[k].append((v_sort,v)) # Don't duplicate pages
#         else:
#             index[k] = [(v_sort,v)] # Add dict entry if not already present
