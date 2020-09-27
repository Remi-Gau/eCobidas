<!-- TOC -->

-   [Why this project](#why-this-project)
-   [Goals and roadmap](#goals-and-roadmap)
-   [Implementation](#implementation)
-   [References](#references)

<!-- /TOC -->

## Why this project

Poor methods and results description hinders the reproducibility and the
replicability of research. It also makes it hard to compare new and old results
and generally increases inefficiency in the research process. This project is
built on the hope that improving methods and results reporting could improve our
research.

See [here](./10-motivations.md) for more background information.

## Goals

**The short term goal of this project is to make the COBIDAS report easier to
use: we want to create a website with a clickable checklist that, at the end,
automatically generates most of the method section of a (f)MRI / (i)EEG / MEG /
PET paper.**

This repository hosts the work that will turn the report published by the
Committee on Best Practices in Data Analysis and Sharing (COBIDAS) of the
organization for human brain mapping (OHBM) into a practical tool for improving
methods and results reporting in (f)MRI, (i)EEG, MEG.

By turning the checklist into a website, users could more rapidly click through
it and provide more of the information recommended by the COBIDAS report. This
would generate a small text file that summarizes what option was chosen for each
item of the checklist. This machine readable file could then be used to
automatically generate part of the methods section of an article.

See [here](./20-goals.md) for more information on our short and long term goals
as well as possible extension to the project. If you are interested by any of
those, [get in touch](../README.md#how-to-reach-us). Many of them do not
necessarily require super-advanced technical skills (except maybe a certain love
for working with spreadsheet and wanting them to be super organized) :wink:.

We are still in development so we are currently using the
[list of required inputs](./inputs/csv/cobidas_neurovault.csv) from
[neurovault](https://www.neurovault.org/) to work on the user interface.


<!-- ```
├── 00-index.md
├── 10-motivations.md
├── 20-goals.md
├── 30-general-organization.md
├── 40-spreadsheet-content.md
├── 50-how-to-render-the-checklist.md
├── 80-how-to-contribute.md
├── 90-contributors.md
└── 99-references.md
``` -->

## Implementation

<!-- TODO -->

The first step of the implementation involves taking a spreadsheet that contains
all the items of the checklist and turning that into a representation that can
efficiently link the metadata about each item to the data imputed by the user.
We are currently using the
[ReproSchema](https://github.com/ReproNim/reproschema) initiative from
[ReproNim](http://www.repronim.org/) to do this. Basically, it means turning
your 'dumb' spreadsheet into an equivalent but 'smarter' representation of it: a
bunch of hierarchically organized json files that link to each other.

On top of the inherent
[advantages](https://github.com/ReproNim/reproschema#30-advantages-of-current-representation)
of this schema representation:

-   its use simplifies the rendering of the checklist by using the
    [schema-ui](https://github.com/ReproNim/schema-ui) made for it,
-   this representation allows specification of user interface options that can
    simplify the user experience: it allows us to specify a branching logic that
    will prevent users to be presented with items that are not relevant to them
    (e.g. answer PET-related questions when they have only run an fMRI study).

See [here](./30-general-organization.md) for more information about how this
whole project is organized.

See [here](./50-how-to-render-the-checklist.md) for more information on how to
work on the checklist on your own computer.

## References

See [here](99-references.md).
