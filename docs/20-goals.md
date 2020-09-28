# Goals

<!-- TOC -->

-   [Goals](#goals)
    -   [Imagined impact on the field of neuroimaging ("pie in the sky" goals)](#imagined-impact-on-the-field-of-neuroimaging-pie-in-the-sky-goals)
    -   [Requirements for the implementation](#requirements-for-the-implementation)
    -   [Milestones (short term goals)](#milestones-short-term-goals)
        -   [MRI COBIDAS](#mri-cobidas)
        -   [M/EEG COBIDAS](#meeg-cobidas)
    -   [Extensions (intermediate goals)](#extensions-intermediate-goals)
        -   [Extended checklists](#extended-checklists)
        -   [Links with BIDS and NIDM](#links-with-bids-and-nidm)
        -   [Links to standarized pipelines (fMRIprep)](#links-to-standarized-pipelines-fmriprep)
        -   [Automatic information extraction from source data (DICOM)](#automatic-information-extraction-from-source-data-dicom)
    -   [Further developments (long term goals)](#further-developments-long-term-goals)
        -   [Link to main neuroimaging software](#link-to-main-neuroimaging-software)
        -   [Link to pipeline-creating tools](#link-to-pipeline-creating-tools)
        -   [Link to journal specific checklists](#link-to-journal-specific-checklists)
        -   [Link to neurolex](#link-to-neurolex)
    -   [Potential applications ("pie in the sky" goals)](#potential-applications-pie-in-the-sky-goals)

<!-- /TOC -->

## Vision

We envision that using checklists to report methods and results can:

1.  provide comprehensive descriptions, in a format that is both human and
    machine-readable, of the data collection and analysis pipelines used in
    published papers: in other words we want an app to help **document**
    pipelines to improve the reproducibility of our work and to reduce
    inefficiencies and frictions when trying to build on each other's work.

1.  facilitate the creation and preparation of pre-registration and registered
    reports by reminding of future analysis steps that we might otherwise
    overlook or forget about: in other words we want an app to help us think
    about and **create** pipelines before we start collecting data.

1.  help make peer-review more objective: we want an app to help us **check**
    pipelines.

1.  facilitate systematic literature reviews and meta-analyses (use the app to
    **read** pipelines)

1.  facilitate data sharing (use the app to **standardize** the report of
    information)

## Milestone

-   short term

-   intermediate

-   long term

## Requirements for the implementation

The implementation of this project should remain flexible enough to:

-   accommodate the inclusion of new items in the checklist as new neuroimaging
    methods mature (e.g. new multivariate analysis, high-resolution MRI...),

-   easily fork the project and convert it to create a checklist-website for a
    different field.
