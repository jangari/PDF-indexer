# PDF Indexer
Generates an end-of-book index from an exported list of PDF annotations

![Cover](images/cover.png)

## Acknowledgements

Written by Aidan Wilson (@jangari) on 2017-09-04 to assist in the generation of an end-of-book index for an academic book.

## About

PDF Indexer Generates tab-delimited text formatted for a book index, with reference and a list of page numbers. Input is a tab-delimited file that has been output from a pdf containing page references and annotations. The expectation is that the user will undertake post-processing work with the generated text, such as separate alphabetic blocks, add cross-references ('see x') and create subheadings (currently not supported here).

## Usage

### Overview

PDF Indexer takes as its input an exported tab-delimited report of a PDF file's comments and their respective page numbers. It is expected that the user will annotate a PDF file, for example a page proof of a book manuscript, and manually (or programmatically, or however they should choose to) annotate index locations with comments. One way to do this is to use Adobe Acrobat to enter comments on the text, and to use Adobe Actions, or another method, to export the comments with their pages numbers. For Mac users, Automator has an action for PDF files that will export PDF annotations, and so a small Automator script could be configured to generate the list of index references.

Begin by opening the PDF file that requires an index in a program such as Adobe Acrobat, Apple Preview, or some other program that allows you to enter notes on the text. Apple Preview is the tool used for the following screenshots but the process is basically the same in other programs and consists of the following:

1. Find a reference to index
1. Highlight it
1. Add a note to it with the desired index text and optionally a page range (if it is a range of pages rather than the single page containing the highlight)
1. When all desired index locations have been annotated, export the annotations to a text file (an automator script can be configured to do this)
1. Optionally fix any annotations in the text file
1. Pass into index script and direct output to text file
1. Thoroughly check index text file for errors

The entire process is demonstrated in the gif below.

![PDF index process](images/PDF_index_process.gif)

### Synopsis

Help text:

```

usage: generate-index.py [-h] [-o OFFSET] [-s SEPARATOR] [-g] [-w] [-l] [-e]
                         [-c] [-t] [-m]
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
                        locator. Default is two spaces.
  -g, --group           Display output entries in alphabetic groups separated
                        by line breaks and (with -gg) section headings.
  -w, --word-sort       Default. Sorts entries using word-by-word alphabetic
                        order (de Marco > dean).
  -l, --letter-sort     Sorts entries using letter-by-letter alphabetic order
                        (dean > de Marco).
  -e, --elide           Elide numbers in page ranges where possible (excluding
                        teens).
  -c, --conjunctions    Ignore conjunctions (of, from, with, and) in sorting
                        subheadings.
  -t, --the             Ignore 'the' when sorting entries.
  -m, --mac             Sorts Mc names (McIntosh) along with corresponding Mac
                        names (MacIntosh).
```

The output will be printed to the shell or can be redirected to a file.

### Page ranges

Page ranges are complex for indexes, and publishers vary in the expected style (for example, eliding common numbers, 134-9). PDF Indexer supports page ranges only through a manual process: the page range should be entered into the annotation in parentheses. PDF Indexer will use this page range instead of the page number associated with the annotation. If your publisher prefers elided page ranges, enter the elided page range explicitly into the PDF comment. 

The fact that the page range string overrides the actual page number of the comment has the corollary effect that page range index references need not be comments on the actual section of the page proof PDF; they could go anywhere. 

A comment in a PDF that pertains to a page range may look like this `humor theory (10-25)` and will be output as `humor theory  10-25`, and will sort correctly with respect to other page references for that index.

PDF Indexer expects a page range of exactly this pattern: two page numbers separated by a dash `-` inside parentheses after the index text and one or more whitespace characters. When PDF Indexer comes across index text matching this pattern, the numbers are parsed out of the text and are used in place of the page number. The index text is also stored without the page range or the trailing whitespace.

So that the sort works properly, PDF Indexer extracts the first page number of the range and uses it as the sort value in the tuple. When outputting page numbers, the tuples in the list are sorted numberically by this sort value, and the page reference value is what is ultimately printed.

### Elision of page ranges

With the `-e/--elide` option enabled, PDF Indexer will elide page numbers where possible. The range `123-126` will be elided to `123-6`, `201-203` to `201-3` and so on. Teens are not elided, so `112-118` is elided to `112-18`. 

This output style is disabled by default.

### Subheadings

PDF Indexer supports subheadings using the syntax `heading <separator> subheading`, where `<separator>` is one of `|`, `:` or `-`. Subheadings are output as an indented list which is itself independently ordered, using the same sorting options configured with the flags `-l`, `-m` and `-t`. Subheading lists are additionally able to be sorted ignoring conjunctions such as `in`, `and`, `of` and so on, using the `-c/--conjunctions` flag discussed below.

Sample output:

```
Australia  65
Argentina  70, 76
comedy
  comedians  13
  humor theory  10, 10-25
  satire  11, 25
computing  34-7
```

This behaviour cannot be suppressed (at the moment). If a PDF annotation contains one of the separators with a space on either side, it will be parsed into an entry and a subheading. Entries that coincidentally contain that string

### Front-matter offset

Depending on the PDF program and method of exporting comments, page numbers may be consistently incorrect due to the presence of frontmatter pages. PDF Indexer has an optional argument `-o/--offset` which sets the amount of frontmatter offset to account for. A negative number may also be entered to account for PDF files that do not start at page 1. You should thoroughly check the output for accuracy and apply this option if needed.

### Grouping output by letter

PDF Indexer supports optional grouping of the output by letter using the flag `-g/--group`. With this flag set, the above example will be output as:

```
Australia  65
Argentina  70, 76

  comedians  13
  humor theory  10, 10-25
  satire  11, 25
computing  34-7
```
Adding a second `-g` flag will also print out the initial letter as a capital. i.e.:

```
A
Australias  65
Argentina  70, 76

C
  comedians  13
  humor theory  10, 10-25
  satire  11, 25
computing  34-7
```

### Word-by-word and letter-by-letter alphabetic sorting

Publishers (and authors) differ as to whether they prefer word-by-word alphabetic order, or letter-by-letter. PDF Indexer will sort output word-by-word by default. Applying the `-l/--letter` flag will enable letter-by-letter sorting. This effectively sorts the index as though there were no spaces or punctuation in the index entry text.

This setting applies to both entries and subentries.

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

`10	computing (10n4)` will be output as `computing	10 n. 4` and `10	computing (10n)` will be output as `computing	10 n.`. As with page ranges, note references will be sorted accurately on the basis of the page number.

### Custom output separator

PDF Indexer supports a custom output field separator using the `-s/--separator` flag. The default is two spaces ("  "), but this could be any string. 

### Ignoring 'The' in entries
Some style guides will recommend sorting the index entries ignoring 'the', for example:

```
W
Warnke, Mike  4
Wiseguys  5
The Wittenburg Door  3
```

PDF Indexer allows for this behaviour using the `-t/--the` flag. Setting this option affects both entries and subentries.

### Ignoring conjunctions in subheading lists

Some style guides will recommend that subheading lists are sorted ignoring conjunctions and prepositions such as 'on', 'of', 'and' and so forth. For example:

```
Mormons
  in America  13
  beliefs  8-9
  and Evangelicals  45
  history  8
```

PDF Indexer supports this using the flag `-c/--conjunctions`. Note that this only affects subheading sorting, and not main entry sorting, although main entries should not typically begin with conjunctions or prepositions, as they are intended to be read as a relationship between the subheading and the main entry.

This behaviour is disabled by default.

### Sorting "Mc" with "Mac"

Traditionally, names such as McCleod, McIntyre and McDonald are sorted as though they were spelled MacCleod, MacIntyre and MacDonald, the reason being that it used to be largely arbitrary which spelling was used, and that it was best to have them sorted along with one another.

PDF Indexer supports this with the `-m/--mac` flag. This sorting will apply both to entries and subentries.

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
