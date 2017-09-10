#!/usr/bin/python

import re, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--offset", type=int, help="Set frontmatter offset for page numbers to be correctly rendered.", dest="OFFSET", default=0)
parser.add_argument("-s", "--separator", type=str, help="Set output field separator between index entry and locator. Default is a tab character.", default="\t", dest="separator")
parser.add_argument("-g", "--group", action="store_true", help="Display output entries in alphabetic groups separated by line breaks and section headings.")
parser.add_argument("-w", "--word-sort", action="store_true", help="Sorts entries using word-by-word alphabetic order (de Marco > dean).", default=False, dest="word")
parser.add_argument("-l", "--letter-sort", action="store_true", help="Sorts entries using letter-by-letter alphabetic order (dean > de Marco). True by default.", default=True, dest="letter")
parser.add_argument("-e", "--elide", action="store_true", help="Elide numbers in page ranges where possible (excluding teens).", dest="elide")
parser.add_argument("-c", "--conjunctions", action="store_true", help="Ignore conjunctions (of, from, with, and) in sorting subheadings.", dest="conjunctions")
parser.add_argument("-t", "--the", action="store_true", help="Ignore 'the' when sorting entries.", dest="ignoreThe")
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

    sk_pattern=re.compile("(.*?)\s\|\s(.*)")
    if re.match(sk_pattern,k):
        sk_match=sk_pattern.search(k)
        k = sk_match.group(1).rstrip().lstrip()
        sk = sk_match.group(2).rstrip().lstrip()
        if k in index:
            if sk in index[k]:
                if not (v_sort,v) in index[k][sk]:
                    index[k][sk]=[(v_sort,v)]
            else:
                index[k][sk]=[(v_sort,v)]
        else:
            index[k]={sk:[(v_sort,v)]}
    else:
        if k in index: # Don't duplicate entries
            if not (v_sort,v) in index[k]:
                index[k].append((v_sort,v)) # Don't duplicate pages
        else:
            index[k] = [(v_sort,v)] # Add dict entry if not already present

stop_words = {"and ": "", "in ": "", "of ": "", "with ": "", "on ": "", "by ": "", "at ": "", "from ": "", "about": ""}
punct = {",": "", " ": "", "'": ""}
def repl_all(text,dic):
    dic = dict((re.escape(k), v) for k, v in dic.items())
    pattern = re.compile("|".join(dic.keys()))
    return pattern.sub(lambda m: dic[re.escape(m.group(0))], text.lower())

def ignore_the(d):
    return sorted(d,key=lambda s: repl_all(s,{'the ':''}).lower())

def word_sort(d):
    return sorted(d,key=lambda s: s.lower())

def letter_sort(d):
    return sorted(d,key=lambda s: repl_all(s,punct).lower())

def ignoreConjunctions(d):
    return sorted(d,key=lambda s: repl_all(s,stop_words).lower())

keys=letter_sort(index)
if args.word:
    keys=word_sort(index)
if args.ignoreThe:
    keys=ignore_the(keys)

k_prev=None


for k in keys:
    if args.ignoreThe:
        k_this=repl_all(k.lower(),{'the ':''})[0].upper()
    else:
        k_this=k[0].upper()
    if type(index[k]) == list:
        vlist=list()
        for vtuple in sorted(index[k]):
            vlist.append(vtuple[1])
        if args.group:
            if k_prev != k_this:
                print("\n"+k_this)
                k_prev = k_this
        print(k+args.separator+','.join(map(str,vlist)))
    else:
        print(k)
        skeys=letter_sort(index[k])
        if args.word:
            skeys=word_sort(index[k])
        if args.conjunctions:
            skeys=ignoreConjunctions(skeys)
        for sk in skeys:
                vlist=list()
                for vtuple in sorted(index[k][sk]):
                    vlist.append(vtuple[1])
                print(" - "+sk+args.separator+','.join(map(str,vlist)))
