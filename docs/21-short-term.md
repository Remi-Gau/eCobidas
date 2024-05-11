# Short term goals

**The short term goal of this project is to make the COBIDAS report (and similar
guidelines) easier to use.** We want to create a prototype website with a
clickable checklist that, at the end, automatically generates most of the method
section of a (f)MRI or (i)EEG / MEG or PET paper.

<hr>

So far the common short goals of all the versions of the app (for MRI, PET...)
are:

-   Create a set of tools and a proof of concept web-app that can:

    -   [x] convert a set of spreadsheet of items into a schema that represents all

    -   [x] from this schema generate a checklist to be clicked through by users,

    -   [x] outputs a set of JSON-LD files once the user is done,

    -   [ ] generate a method section using these JSON-LD files and some boilerplate
            template of a method section where the content of the JSON-LD files
            could be reinjected.

<hr>

For the spreadsheets that represent the recommendation guidelines, the initial
curation process must:

-   identify high-priority items for each checklist,

-   ensure that those high priority items has been properly atomized (meaning
    that it is only made of a single question) and curated (define an item name,
    a question, the type of response expected and an eventual list of response
    choices).

<!-- TODO  Add link to spreadsheet doc -->

<hr>

## MRI

The current version of MRI prototype is inspired from
[Neurovault](https://neurovault.org/), so we would have to expand from there.

The goal for the MRI app would to be able to describe a typical fMRI study with:

-   a single functional task
-   one anatomical scan
-   using mass uni-variate analysis

## M/EEG

The MRI version is currently ahead and the work done there can pave the way for
the MEEG version.

The MEEG COBIDAS guidelines have recently been published (see the
[preprint](https://osf.io/a8dhx/) and
[webpage](https://cobidasmeeg.wordpress.com/)).

The main short term goals for the MEEG version are:

-   [x] Identify overlaps between the MEEG and the MRI spreadsheets and harmonize
    both versions by extracting the common parts into standalone spreadsheets:
    for example there could be one common spreadsheet for participant sample
    description.

-   [ ] Consolidate the other items of the spreadsheet, as it is still missing a lot
    of information

-   [ ] Identify high-priority items in the checklist (similar to Carp 2012 for
    fMRI, e.g.
    [Luck & Gaspelin 2015](https://doi.org/10.1111/psyp.12639))

## Positron emission tomography and Eyetracking

Those 2 projects are more quite ahead already as they both started from fairly
standardized spreadsheets.

Both could benefit from a better definition of the response types and response options.
