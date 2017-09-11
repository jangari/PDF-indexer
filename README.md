# PDF Indexer
Generates an end-of-book index from an exported list of PDF annotations

## Acknowledgements

Written by Aidan Wilson (@jangari) on 2017-09-04 to assist in the generation of an end-of-book index for an academic book.

## About

PDF Indexer Generates tab-delimited text formatted for a book index, with reference and a list of page numbers. Input is a tab-delimited file that has been output from a pdf containing page references and annotations. The expectation is that the user will undertake post-processing work with the generated text, such as separate alphabetic blocks, add cross-references ('see x') and create subheadings (currently not supported here).

## Usage

### Overview

PDF Indexer takes as its input an exported tab-delimited report of a PDF file's comments and their respective page numbers. It is expected that the user will annotate a PDF file, for example a page proof of a book manuscript, and manually (or programmatically, or however they should choose to) annotate index locations with comments. One way to do this is to use Adobe Acrobat to enter comments on the text, and to use Adobe Actions, or another method, to export the comments with their pages numbers. For Mac users, Automator has an action for PDF files that will export PDF annotations, and so a small Automator script could be configured to generate the list of index references.

### Annotating a PDF

Begin by opening the PDF file that requires an index in a program such as Adobe Acrobat, Apple Preview, or some other program that allows you to enter notes on the text. Apple Preview is the tool used for the following screenshots but the process is basically the same in other programs and consists of the following:

1. Find a reference to index
1. Highlight it
1. Add a note to it with the desired index text and optionally a page range (if it is a range of pages rather than the single page containing the highlight)

The preview sidebar can be set to show all highlights and their notes from the View menu.

![find-a-reference][screenshot1]
![highlight][screenshot2]
![annotate][screenshot3]
![view_annotations][screenshot4]

[screenshot1]:images/screenshot1.png
[screenshot2]:images/screenshot2.png
[screenshot3]:images/screenshot3.png
[screenshot4]:images/screenshot4.png

When you have fully annotated your document, you need to find a way to export those annotations. There may be several methods. One that I have used is to configure an Automator application that takes a pdf file and runs the 'Export PDF Annotations' action. 

Here is a very brief example of a list of index references that is output by this process.

```
10	humor theory
11	satire
13	comedians
15	satire
```

This kind of format is not suitable for an index. An index is an alphabetically sorted list of index terms (such as *comedy*, *satire* in the example here) followed by an exhaustive list of page numbers or ranges. PDF Indexer generates that format from the exported PDF annotations. The above, therefore, will generate:

```
comedians	13
humor theory	10
satire	11, 15
```

The user will then need to undertake some post-processing to prepare this text for their publisher. They will need to separate it into alphabetic blocks, construct any desired (sub)-heading hierarchy, and they should also conduct thorough quality control before submitting the index to their publisher. PDF Indexer only collates and sorts the indexes from a single page reference per line, to a proper index style with an index reference and a list of page references.

### Synopsis

Help text:

```
usage: generate-index.py [-h] [-o OFFSET] [-s SEPARATOR] [-g] [-w] [-l] [-e]
                         [-c] [-t]
                         input_file

positional arguments:
  input_file

optional arguments:
  -h, --help            show this help message and exit
  -o OFFSET, --offset OFFSET
                        Set frontmatter offset for page numbers to be
                        correctly rendered.
  -s SEPARATOR, --separator SEPARATOR
                        Set output field separator between index entry and
                        locator. Default is a tab character.
  -g, --group           Display output entries in alphabetic groups separated
                        by line breaks and section headings.
  -w, --word-sort       Default. Sorts entries using word-by-word alphabetic
                        order (de Marco > dean).
  -l, --letter-sort     Sorts entries using letter-by-letter alphabetic order
                        (dean > de Marco).
  -e, --elide           Elide numbers in page ranges where possible (excluding
                        teens).
  -c, --conjunctions    Ignore conjunctions (of, from, with, and) in sorting
                        subheadings.
  -t, --the             Ignore 'the' when sorting entries.
```

The output will be printed to the shell or can be redirected to a file.

### Page ranges

Page ranges are complex for indexes, and publishers vary in the expected style (for example, eliding common numbers, 134-9). PDF Indexer supports page ranges only through a manual process: the page range should be entered into the annotation in parentheses. PDF Indexer will use this page range instead of the page number associated with the annotation. If your publisher prefers elided page ranges, enter the elided page range explicitly into the PDF comment. 

The fact that the page range string overrides the actual page number of the comment has the corollary effect that page range index references need not be comments on the actual section of the page proof PDF; they could go anywhere. 

A comment in a PDF that pertains to a page range may look like this `humor theory (10-25)` and will be output as `humor theory	10-25`, and will sort correctly with respect to other page references for that index.

PDF Indexer expects a page range of exactly this pattern: two page numbers separated by a dash `-` inside parentheses after the index text and one or more whitespace characters. The regular expression for this capture is `.*\s+\(([0-9]+-[0-9]+)\)`. When PDF Indexer comes across index text matching this expression, the numbers are parsed out of the text and are used in place of the page number. The index text is also stored without the page range or the trailing whitespace.

So that the sort works properly, PDF Indexer extracts the first page number of the range and uses it as the sort value in the tuple. When outputting page numbers, the tuples in the list are sorted numberically by this sort value, and the page reference value is what is ultimately printed.

### Elision of page ranges

With the `-e/--elide` option enabled, PDF Indexer will elide page numbers where possible. The range `123-126` will be elided to `123-6`, `201-203` to `201-3` and so on. Teens are not elided, so `112-118` is elided to `112-18`. 

This output style is disabled by default.

### Subheadings

Back-of-book indexes often contain subheadings of index references. The above example might be output as follows (extended for other headings not within comedy):

```
Australia	65
Argentina	70, 76
comedy
   comedians	13
   humor theory	10, 10-25
   satire	11, 25
computing	34-37
```

This format is not currently support by default by PDF Indexer, however a simple manual workaround exists. Prepend the annotations of subheadings with their outer heading and a meaningful separator, such as a pipe `|` character, as follows:

```
10	comedy | humor theory
10	comedy | humor theory (10-25)
11	comedy | satire
13	comedy | comedians
15	comedy | satire
34	computing (34-37)
65	Australia
70	Argentina
76	Argentina
```

As PDF Indexer sorts the index keys alphabetically, these subheadings will appear adjacent to one another and so converting these into a top-level heading and subheadings will be a trivial modification:

```
Australia	65
Argentina	70, 76
comedy | comedians	13
comedy | humor theory	10, 10-25
comedy | satire	11, 25
computing	34-37
```

### Front-matter offset

A known-issue is that PDF comments contain page references beginning from the start of the PDF file, and those page numbers may differ from the actual page numbers due to the presence of front-matter. PDF Indexer has an optional argument `-o/--offset` which sets the amount of frontmatter offset to account for. A negative number may also be entered to account for PDF files that do not start at page 1.

A future version of this script would calculate the offset needed by parsing the PDF document.

### Grouping output by letter

PDF Indexer supports optional grouping of the output by letter using the flag `-g/--group`. With this flag set, the above example will be output as:

```
A
Australia	65
Argentina	70, 76

C
comedy | comedians	13
comedy | humor theory	10, 10-25
comedy | satire	11, 25
computing	34-37
```

This output style is disabled by default.

### Word-by-word and letter-by-letter alphabetic sorting

Publishers (and authors) differ as to whether they prefer word-by-word alphabetic order, or letter-by-letter. PDF Indexer supports both outputs with the `-l` (letter sort, default) and `-w` (word sort) flags.

#### Word-by-word sort order

  - de Maria
  - dean
  - dematerial
  - I, Robot
  - In a pinch
  - Isaacs

#### Letter-by-letter

  - dean
  - de Maria
  - dematerial
  - In a pinch
  - I, Robot
  - Isaacs

### Note indexing

Indexes pointing to notes are supported in the same manner as page ranges, by using a string page reference in place of the page number as exported from the PDF.

To reference a note, enter the page number for the reference followed by `n` and optionally, the note number if there are multiple notes. E.g.:

`10	computing (10n4)` will be output as `computing	10n4` and `10	computing (10n)` will be output as `computing	10n`. As with page ranges, note references will be sorted accurately on the basis of the page number.

### Custom output separator

PDF Indexer supports a custom output field separator using the `-s/--separator` flag. The default is a tab character, but this could be any string.

### Subheadings
PDF Indexer supports subheadings using the syntax `heading | subheading`. Subheadings are output as an indented list which is itself independently ordered. Subheading lists are additionally able to be sorted ignoring conjunctions such as in, and, of and so on., using the `-c/--conjunctions` flag discussed below.

### Ignoring 'The' in entries
Some style guides will recommend sorting the index entries ignoring 'the', for example:

```
W
Warnke, Mike    4
Wiseguys    5
The Wittenburg Door 3
```

PDF Indexer follows this behaviour using the `-t/--the` flag. Default behaviour is to sort the index for occurrences of 'the'.

### Ignoring conjunctions in subheading lists

Some style guides will recommend that subheading lists are sorted ignoring conjunctions and prepositions such as 'on', 'of', 'and' and so forth. For example:

```
Mormons
 - in America   13
 - beliefs 8-9
 - and Evangelicals	45
 - history    8
```

PDF Indexer supports this using the flag `-c/--conjunctions`. Note that this only affects subheading sorting, and not main entry sorting, although main entries should not typically begin with conjunctions or prepositions, as they are intended to be read as a relationship between the subheading and the main entry.

This behaviour is disabled by default.

## Limitations

### No support for multiple index styles

Currently only a single output style is supported, with index references separated from page number lists with a tab character. Support for different styles (particularly the run-on style) may be added at a later stage. This only practically affects subheadings at this stage.  

### No support for cross-references

PDF Indexer does not currently support cross-referencing. Cross-references within the index (such as *New Holland	see Australia*) must be entered manually as a post-processing step. It is not clear that there is much benefit to including this functionality, since providing support for cross-references would not save the user any time, as they would have to be manually annotated in the PDF anyway. The only potential for efficiency here is if PDF Indexer automatically provided cross references to subheadings, where a PDF annotation such as:

```
11	comedy | satire
```

might yield:

```
comedy
[...]
    satire  11
[...]
satire  see comedy
```

However it is not clear that this behaviour would be desired. It would also be contingent on the implementation of subheadings.
