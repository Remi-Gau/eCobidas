# Short term goals

**The short term goal of this project is to make the COBIDAS report easier to
use: we want to create a website with a clickable checklist that, at the end,
automatically generates most of the method section of a (f)MRI or (i)EEG / MEG
paper.**

## MRI COBIDAS

So far the short goals of the MRI app have been:

-   Create a proof of concept webapp that can:

    -   can generate a checklist to clicked through by users, given a template
        spreadsheet file, :heavy_check_mark: :smiley:

    -   outputs a populated JSON file once the user is done, :heavy_check_mark:
        :smiley:

    -   generate a method section using this JSON file.

By working on those first steps, a proof of concept app has been put together.
There is now work to be done to extend what this app can do so we can have a
first release that could be used for a typical fMRI study with:

-   a single functional task

-   one anatomical scan

-   using mass uni-variate analysis

To reach that first milestone we still need to work on the following issues:

-   Identify high-priority items that at least include those from
    [Carp 2012](https://www.ncbi.nlm.nih.gov/pubmed/22796459) to make sure users
    do better than 50% of the papers reported in this study

-   Create a version of the spreadsheet where each of those high priority items
    has been properly atomized (i.e. it is only composed of a single question)

-   Identify ways in which the user experience can be improved, mostly by
    finding ways to minimize the time users have to spend using the app.

-   Identify defaults in the most common software packages (SPM, FSL, AFNI) to
    inform users about potential answers

## M/EEG COBIDAS

The MRI version is currently ahead and the work done there can pave the way for
the MEEG version.

The MEEG COBIDAS guidelines have recently been published (see the
[preprint](https://osf.io/a8dhx/) and
[webpage](https://cobidasmeeg.wordpress.com/)).

The main short term goals for the MEEG version are:

-   Identify overlaps between the MEEG and the MRI spreadsheets and harmonize
    both versions by extracting the common parts into standalone spreadsheets:
    for example there could be one common spreadsheet for participant sample
    description.

-   Identify high-priority items in the checklist (similar to Carp 2012 for
    fMRI, e.g.
    [Luck & Gaspelin 2015](https://onlinelibrary.wiley.com/doi/full/10.1111/psyp.12639))

-   Create a version of the spreadsheet where each of those high priority items
    has been properly atomized (i.e it is only composed of a single question)

## Positron emission tomography

## Eyetracking
