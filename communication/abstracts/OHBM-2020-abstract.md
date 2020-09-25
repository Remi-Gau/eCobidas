# eCOBIDAS - Abstract OHBM 2020

## Title

eCOBIDAS: a webapp checklist to improve neuroimaging methods and results
reporting

## Authors

If you have participated directly or indirectly to this project and you would
like to be added as author, please create a profile on the OHBM 2020 abstract
submission site (https://ww4.aievolution.com/hbm2001/), and add your name below:

-   Rémi Gau
-   Tom Nichols
-   Cassandra Gould van Praag
-   Satrajit Ghosh
-   Sanu Ann Abraham
-   Kristina Wiebels
-   Zsuzsika Sjoerds
-   David Moreau

## Intro

In any scientific study, a complete and precise method section is necessary to
understand and evaluate the results, plan replications, seed new research and
compare outcomes across studies. However, a large number of neuroimaging studies
fail to report important details necessary for independent investigators to
achieve these goals [1]. In order to improve this situation, the Committee on
Best Practices in Data Analysis and Sharing (COBIDAS) of OHBM released a report
to establish a set of best practices for methods and results reporting in f/MRI
research [4]. This has been recently followed by a similar initiative for EEG
and MEG [5]. The COBIDAS reports are accompanied by checklist tables meant to
help authors ensure that their methods and results description complies with the
Committee’s recommendations. These checklists are a valuable resource, but the
static PDF tables do not lend themselves to an actionable format, and users may
be required to scroll through pages of items that do not concern their specific
use-case. Moreover, while these checklists help generate a human readable method
section, they do not provide ways to create a machine-readable equivalent that
would encapsulate a large part of the metadata in a study. The goal of the
eCOBIDAS webapp is to provide a user-friendly solution for researchers to fill
out the COBIDAS checklists, while generating a machine-readable summary of a
method section. This summary can then be used to automate method section writing
for authors, or to facilitate the assessment of a study quality during
peer-review.

## Methods

The tables of the COBIDAS reports were reduced to600 individual items. A subset
of items was selected and converted into a hierarchical schema representation in
accordance with the repronim schema (https://github.com/ReproNim/reproschema).
The use of this schema representation offers several advantages, as it allows:
Efficient linking between the metadata about each item and the data provided by
the user; Enforcing of output format consistency and of input validation
directly at the data acquisition stage (i.e., while the user is filling out the
checklist); Specifying user interface details for certain use-cases (e.g., to
let users be presented only with items or sections that concern them). We then
adapted the JavaScript-based webapp used for the visualization of the repronim
schema to allow users to browse and complete each section of the checklist.

## Results

The development of the webapp started at the OHBM Hackathon 2019 and aims to be
a project developed by the community for the community. All information is
centralized on an open science framework project [2]. The current prototype of
the webapp can be accessed at https://cobidas-checklist.herokuapp.com/#/. It is
based on the 88 metadata items available to characterise a collection of
neuroimaging results uploaded on the neurovault website [3]. This only
constitutes a subset of the full f/MRI COBIDAS checklist and will be expanded in
the near future. Users can fill out the different sections of the checklist
(study design, participants, preprocessing, etc.) and are only presented with
items that concern their use-case. Finally, the output can be exported in a set
of machine-readable JSON files.

## Conclusion

Future developments of the webapp will involve:

-   Expansion of the list of items covered to include at first all the items
    from Carp 2012, and then the entirety of the COBIDAS f/MRI checklist;
-   Establish a list of recommended MEEG items to create a version for
    electrophysiology studies
-   Automatically generate a PDF summary and a method section after the
    checklist has been filled
-   Automatically fill the checklist by allowing the application to query the
    content of:
    -   a BIDS dataset
    -   an SPM or FSL analysis pipeline (matlabbatch.mat or design.fsf).

eCOBIDAS is part of a broader trend towards open and reproducible science, to
facilitate valid and robust inferences in neuroscience. We encourage any member
of the community to contribute to this project.

## Categories

-   Informatics others
-   Workflow
-   Other methods
-   Keywords
-   Checklist
-   Workflows
-   Statistical methods
-   Webapp
-   Machine-reading
-   Standardization
-   COBIDAS
-   Transparency
-   Replicability
-   Reproducibility

## Reference

[1] Carp J. (2018), ‘The secret lives of experiments: Methods reporting in the
fMRI literature’, NeuroImage. vol. 63, no. 1, pp. 289-300, doi:
10.1016/j.neuroimage.2012.07.004

[2] Gau, Remi et al (2019), ‘COBIDAS Checklist’, OSF, doi: 10.17605/OSF.IO/ANVQY

[3] Gorgolewski K. J. (2015) et al. ‘NeuroVault.org: a web-based repository for
collecting and sharing unthresholded statistical maps of the brain’, Frontiers
in Neuroinformatics. vol. 9, no. 8 doi: 10.3389/fninf.2015.00008

[4] Nichols T. E. et al. (2017), ‘Best Practices in Data Analysis and Sharing in
Neuroimaging using MRI’, Nature Neuroscience, vol. 20, no 3, pp. 299-303, doi:
10.1038/nn.4500.

[5] Pernet, C. R. et al. (2018), Best Practices in Data Analysis and Sharing in
Neuroimaging Using MEEG, OSF Preprints, August 9. doi:10.31219/osf.io/a8dhx
