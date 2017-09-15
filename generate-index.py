#!/usr/bin/python

import re, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--offset", type=int, help="Set frontmatter offset for page numbers to be correctly rendered.", dest="offset", default=0)
parser.add_argument("-s", "--separator", type=str, help="Set output field separator between index entry and locator. Default is two spaces.", default="  ", dest="separator")
parser.add_argument("-g", "--group", action="count", help="Display output entries in alphabetic groups separated by line breaks and (with -gg) section headings.")
parser.add_argument("-w", "--word-sort", action="store_true", help="Default. Sorts entries using word-by-word alphabetic order (de Marco > dean).", default=True, dest="word")
parser.add_argument("-l", "--letter-sort", action="store_true", help="Sorts entries using letter-by-letter alphabetic order (dean > de Marco).", default=False, dest="letterSort")
parser.add_argument("-e", "--elide", action="store_true", help="Elide numbers in page ranges where possible (excluding teens).", dest="elide")
parser.add_argument("-c", "--conjunctions", action="store_true", help="Ignore conjunctions (of, from, with, and) in sorting subheadings.", dest="conjunctions")
parser.add_argument("-t", "--the", action="store_true", help="Ignore 'the' when sorting entries.", dest="ignoreThe")
parser.add_argument("-m", "--mac", action="store_true", help="Sorts Mc names (McIntosh) along with corresponding Mac names (MacIntosh).", dest="sortMac")
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
OFFSET=args.offset

for line in comments_file:
    v,k = line.split('\t') # Split index reference into page ref and text
    k = k.rstrip() # Strip any whitespace
    v = int(v)-OFFSET
    v_sort = v # For single pages, v_sort is simply v.

    pattern = re.compile("(.*)\s+\(([0-9]+(n[0-9]*|\-[0-9]+))\)")
    if re.match(pattern,k):
        match = pattern.search(k)
        k = match.group(1)
        v = match.group(2)
        vp = re.compile("([0-9]+)(-|n)") # Parse the start number of the page range to be the sort value
        vm = vp.search(v)
        v_sort = int(vm.group(1))

        if 'n' in v:
	    n_pattern=re.compile("([0-9]+)n([0-9]+)?")
	    n_match=n_pattern.search(v)
	    v=n_match.group(1)
	    n=n_match.group(2)
	    if n == None:
		v = v+" n."
	    else:
		v = v+' n. '+n

        if args.elide and '-' in v:
            vstart, vend = v.split('-')
            vstart, vend = elide(vstart,vend)
            v = vstart+"-"+vend

    sh_pattern=re.compile("(.*?)\s?[:\|-]\s(.*)")
    if re.match(sh_pattern,k):
        sh_match=sh_pattern.search(k)
        k = sh_match.group(1).rstrip().lstrip()
        sk = sh_match.group(2).rstrip().lstrip()
        if not k in index:
            index[k]={'entry':[],'subentries':{}}
        if sk in index[k]['subentries']:
            if (v_sort,v) not in index[k]['subentries'][sk]:
                index[k]['subentries'][sk].append((v_sort,v))
        else:
            index[k]['subentries'][sk]=[(v_sort,v)]
    elif not k in index:
            index[k]={'entry':[(v_sort,v)],'subentries':{}}
    elif (v_sort,v) not in index[k]['entry']:
        index[k]['entry'].append((v_sort,v))

def repl_all(text,dic):
    if len(dic) == 0:
        return text
    else:
        dic = dict((re.escape(k), v) for k, v in dic.items())
        pattern = re.compile("|".join(dic.keys()))
        return pattern.sub(lambda m: dic[re.escape(m.group(0))], text)

def dic_sort(dic,letterSort=False,ignoreThe=False,ignoreConj=False,sortMac=False):
    conjunctions={}
    punct={'"':''}
    the={}
    mac={}
    if ignoreConj:
        conjunctions={"and ": "", "in ": "", "of ": "", "with ": "", "on ": "", "by ": "", "at ": "", "from ": "", "about ": "", "as ": ""}
    if ignoreThe:
        the={"the ":""}
    if letterSort:
        punct={",": "", " ": "", "'": "", '"':''}
    if sortMac:
        mac={"Mc":"Mac"}
    return sorted(dic, key=lambda s: repl_all(repl_all(repl_all(repl_all(s,mac).lower(),conjunctions),the),punct))

k_prev=None

keys = dic_sort(index, letterSort=args.letterSort, ignoreThe=args.ignoreThe, sortMac=args.sortMac, ignoreConj=args.conjunctions)
for k in keys:
    if args.ignoreThe:
        k_this=repl_all(repl_all(k.lower(),{'"':''}),{'the ':''})[0].upper()
    else:
        k_this=repl_all(k,{'"':''})[0].upper()
    vlist=[]
    for v_sort,v in sorted(index[k]['entry']):
        vlist.append(v)
    if args.group > 0 and k_prev != k_this:
        print("")
        if args.group == 2:
            print(k_this)
        k_prev = k_this
    print(k+args.separator+', '.join(map(str,vlist)))
    for subentry in dic_sort(index[k]['subentries'], letterSort=args.letterSort, ignoreThe=args.ignoreThe, ignoreConj=args.conjunctions, sortMac=args.sortMac):
        vlist=[]
        for v_sort,v in sorted(index[k]['subentries'][subentry]):
            vlist.append(v)
        print('  '+subentry+args.separator+', '.join(map(str,vlist)))
