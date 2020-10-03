# Goals

By turning recommendations and guidelines into a series of checklists hosted on
a website, users could more rapidly click through it and provide more of the
recommended information. This would generate a small text file that summarizes
what option was chosen for each item of the checklist. This machine readable
file could then be used to automatically generate part of the methods section of
an article.

But, if done right, this could also in the long term enhance the adoption of
emerging neuroimaging standards (BIDS, fMRIprep, NIDM...), facilitate data
sharing and pre-registration, help with peer-review...

## Vision

We envision that using checklists to report methods and results can:

1.  provide comprehensive human and machine readable descriptions of the data
    collection and analysis pipelines used in published papers: in other words
    we want an app to help **document** pipelines to improve the reproducibility
    of our work and to reduce inefficiencies and frictions when trying to build
    on each other's work.

1.  facilitate the creation and preparation of pre-registration and registered
    reports by reminding of future analysis steps that we might otherwise
    overlook or forget about: in other words we want an app to help us think
    about and **create** pipelines before we start collecting data.

1.  help make peer-review more objective: we want an app to help us **check**
    pipelines.

1.  facilitate systematic literature reviews and meta-analyses (use the app to
    **read** pipelines)

1.  facilitate data sharing (use the app to **standardize** the report of
    information on a pipeline)

## Constraints

The implementation of this project should remain flexible enough to:

-   accommodate the inclusion of new items in the checklist as new methods
    mature (e.g. new multivariate analysis, high-resolution MRI...),

-   easily fork the project and convert it to create a checklist-website for a
    different field.

## Milestones

We are trying to divide our goals and milestones in 3 main categories:

-   [short term](./21-short-term.md)
-   [intermediate](./22-mid-term.md)
-   [long term](./23-long-term.md)
