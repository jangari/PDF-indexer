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

The user will then need to undertake some post-processing to prepare this text for their publisher. They will need to separate it into alphabetic blocks, correct the ordering of page ranges (see limitations below), and construct any desired (sub)-heading hierarchy. They should also conduct thorough quality control before submitting the index to their publisher.

### Synopsis

`python generate-index.py INPUT_FILE [-o/--offset OFFSET]`

The output will be printed to the shell or can be redirected to a file.

### Page ranges

Page ranges are complex for indexes, and publishers vary in the expected style (for example, eliding common numbers, 134-9). PDF Indexer supports page ranges only through a manual process: the page range should be entered into the annotation in parentheses. PDF Indexer will use this page range instead of the page number associated with the annotation. If your publisher prefers elided page ranges, enter the elided page range into the PDF comment. 

The fact that the page range string overrides the actual page number of the comment has the corollary effect that page range index references need not be comments on the actual section of the page proof PDF; they could go anywhere. 

A comment in a PDF that pertains to a page range may look like this (and for completeness, let's suppose it occurs on page 10 of the PDF):

`humor theory (10-25)`

PDF Indexer expects a page range of exactly this pattern: two page numbers separated by a dash `-` inside parentheses after the index text and one or more whitespace characters. The regular expression for this capture is `.*\s+\(([0-9]+-[0-9]+)\)`. When PDF Indexer comes across index text matching this expression, the numbers are parsed out of the text and are used in place of the page number. The index text is also stored without the page range or the trailing whitespace.

So that the sort works properly, PDF Indexer extracts the first page number of the range and uses it as the sort value in the tuple. When outputting page numbers, the tuples in the list are sorted numberically by this sort value, and the page reference value is what is ultimately printed.

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

### Command-line support for front-matter offset

A known-issue is that PDF comments contain page references beginning from the start of the PDF file, and those page numbers may differ from the actual page numbers due to the presence of front-matter. PDF Indexer has an optional argument `-o/--offset` which sets the amount of frontmatter offset to account for. A negative number may also be entered to account for PDF files that do not start at page 1.

A future version of this script would calculate the offset needed by parsing the PDF document.

## Limitations

### Page ranges cannot sort

**This has now been implemented** by refactoring the list of page numbers as a tuple `t`, consisting of a sort value `t[0]` and the page reference `t[1]`. The sort value is used for sorting the list of numbers, and the page reference is what is ultimately printed.

### No support for subheadings

As mentioned above, there is no built-in support for subheadings, but see above for a simple workaround. A future version will accept the `|`-separated comment as suggested above, and render the output with a top-level heading with subheadings.

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
