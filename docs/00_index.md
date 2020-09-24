<!-- TOC -->
<!-- lint disable -->
-   [Why this project](#why-this-project)
-   [Goals and roadmap](#goals-and-roadmap)
-   [Implementation](#implementation)
-   [References](#references)
<!-- lint enable -->
<!-- /TOC -->

## Why this project

Poor methods and results description hinders the reproducibility and the
replicability of research. It also makes it hard to compare new and old results
and generally increases inefficiency in the research process. This project is
built on the hope that improving methods and results reporting could improve our
research.
Please indicate shortly, how do you think Brainhack contributed to diversity and inclusivity in the scientific community?
See [here](./why_this_project.md) for more background information.

## Goals and roadmap

**The short term goal of this project is to make the COBIDAS report easier to
use: we want to create a website with a clickable checklist that, at the end,
automatically generates most of the method section of a (f)MRI or EEG / MEG
paper.**

This repository hosts the work turning the report published by the Committee on
Best Practices in Data Analysis and Sharing (COBIDAS) of the organization for
human brain mapping (OHBM) into a practical tool for improving methods and
results reporting in (f)MRI, (i)EEG, and MEG.

By turning the checklist into a website users could more rapidly click through
it and provide more of the information requested by the COBIDAS report. This
would generate a small text file (a json file) that summarizes what option was
chosen for each item of the checklist. This machine readable file could then be
used to automatically generate part of the methods section of an article.

This repository is a place where:

1. issues and ideas around reaching this goal are discussed

2. plans for how to reach this goal are designed and implemented.

See [here](./goals.md) for more information on our short and long term goals as
well as possible extension to the project. If you are interested by any of
those, get in touch. Many of them do not necessarily require super-advanced
technical skills (except maybe a certain love for working with spreadsheet and
wanting them to be super organized) :wink:.

We are still in development so we are currently using the
[list of required inputs](./xlsx/metadata_neurovault.csv) from
[neurovault](https://www.neurovault.org/) to work on the user interface.

## Implementation

The prototype app for this checklist can be found here:
https://cobidas-checklist.herokuapp.com/

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

See [here](./general_organization.md) for more information about how this whole
project is organized

See [here](./how_to_render_the_checklist.md) for more information on how to work
on the checklist on your own computer.

## References

Jeanette Mumford has a
[30 min video](https://www.youtube.com/watch?v=bsM4KowO5Vc&t=175s) explaining
the background behind the COBIDAS report and giving a run through of the
checklist.

The COBIDAS report:

-   [for MRI and fMRI](https://www.biorxiv.org/content/10.1101/054262v2)

-   [for EEG and MEG](https://osf.io/a8dhx/)

-   MEEG report presentation at
    [OHBM 2019](https://www.pathlms.com/ohbm/courses/12238/sections/15843/video_presentations/138196)

The original [spreadsheet version](https://osf.io/qkb9t/) of the COBIDAS
checklist (thanks to [Cass](https://github.com/cassgvp)!!!)

Presentation slides made about this project can be found in the
[presentations folder](./presentations) and [here](./presentations/links.md).

Other checklists:

-   [Checklist for Artifical Intelligence in Medical Imaging](https://claim.shinyapps.io/CLAIM/)

-   [Consensus on the reporting and experimental design of clinical and cognitive-beharioural neurofeedback studies](https://crednf.shinyapps.io/CREDnf/)

-   [Transparency Checklist](http://www.shinyapps.org/apps/TransparencyChecklist/)
