# PDF Indexer
Generates an end-of-book index from an exported list of PDF annotations

## Acknowledgements

Written by Aidan Wilson (@jangari) on 2017-09-04 to assist in the generation of an end-of-book index for an academic book.

## About

PDF Indexer Generates tab-delimited text formatted for a book index, with reference and a list of page numbers. Input is a tab-delimited file that has been output from a pdf containing page references and annotations. The expectation is that the user will undertake post-processing work with the generated text, such as separate alphabetic blocks, add cross-references ('see x') and create subheadings (currently not supported here).

## Usage

### Overview

PDF Indexer takes as its input an exported tab-delimited report of a PDF file's comments and their respective page numbers. It is expected that the user will annotate a PDF file, for example a page proof of a book manuscript, and manually (or programmatically, or however they should choose to) annotate index locations with comments. One way to do this is to use Adobe Acrobat to enter comments on the text, and to use Adobe Actions to export the comments with their pages numbers, or another method to output comments. For Mac users, Automator has an action for PDF files that will export PDF annotations, and so a small Automator script could be configured to generate the list of index references.

Here is a very brief example of a list of index references.

```
10	humor theory
11	satire
13	comedians
15	satire
```

This kind of format is not suitable for an index. An index would have an alphabetically sorted list of index terms (such as **comedy**, **satire** in the example here) followed by an exhaustive list of page numbers. PDF Indexer generates that format from the exported PDF annotations. The above, therefore, will generate:

```
comedians	13
humor theory	10
satire	11, 15
```

The user will then need to undertake some post-processing to prepare this text for their publisher. They will need to separate it into alphabetic blocks, correct the ordering of page ranges (see limitations below), and construct any desired (sub)-heading hierarchy. They should also conduct thorough quality control before submitting the index to their publisher.

### Synopsis

`python generate-index.py input_file`

The output will be printed to the shell or can be redirected to a file.

### Page ranges

Page ranges are complex for indexes, and publishers vary in the expected style. PDF Indexer supports page ranges only through a manual process: the page range should be entered into the annotation in parentheses. PDF Indexer will use this page range instead of the page number associated with the annotation. This has the corollary effect that page range index references need not be comments on the actual section of the page proof PDF; they could go anywhere. 

A comment in a PDF that pertains to a page range may look like this (and for completeness, let's suppose it occurs on page 10 of the PDF):

`humor theory (10-25)`

PDF Indexer will use the string `10-25` instead of the supplied page number `10` as the value for that index. The page range will be inserted into the list of page numbers as a string, and will thus not be correctly numerically sorted with respect to the rest of the page numbers. So the TO-DO section for a potential future fix.

### Subheadings

Back-of-book indexes often contain headings of index references. The above example might be output as follows (extended for other headings not within comedy):

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
As page ranges (such as 10-25) cannot be coerced into an integer, they cannot be sorted within the list of page references. In a future version, each list entry could be a tuple, with a sort key, usually the same as the page number, but for page ranges, the sort key will be filled by the integer of the first part of the range.

`{'comedy | humor theory':[(10,'10'),(10,'10-25')]}`

This data structure would allow for the list of tuples to be sorted accurately, even where the value (the page reference) is a string.

### No support for subheadings

As mentioned above, there is no built-in support for subheadings, but see above for a simple workaround. A future version will accept the `|`-separated comment as suggested above, and render the output with a top-level heading with subheadings.

## To-Do

### Support for multiple index styles

Currently only a single output style is supported, with index references separated from page number lists with a tab character. Support for different styles (particularly the run-on style) may be added at a later stage. This only practically affects subheadings at this stage.  
