# "pie in the sky" goals

On the long term, we want those web-app to integrate better with other data
standards and softwares to further reduce how much manual entry is required from the user.

Similarly we want to broaden the use-cases for the app.

## Improve user-friendliness

### Improving default answers

If some data is gathered about the content of the method section of a sample of articles in the literature
(see
[Carp, 2012](https://www.ncbi.nlm.nih.gov/pubmed/22796459) or the [eyetracking guidelines](https://psyarxiv.com/f6qcy/)),
it should be possible to create or better organize list of response choices.
It will take less time for users to tick a box rather than type something.
Similarly we could decide to make the most common choices or the "better" option more prominent in a list of response options.

### Adding a help section for each item

The content of some item might be quite obscure for some users, so embedding some help about each item would be a desirable goal.

## Integration with the main neuroimaging software

### Plugins

A side branch of this project includes developing plugins for the main
neuroimaging software toolboxes (SPM, FSL, AFNI).
Such a plugin would receive
processing batch files as input (e.g `matlabbatch.mat` for SPM or `design.fsf`
for FSL) and would create output files (e.g. in json format) readable by the
checklist website, which in turn would be able to display the neuroimaging
processing pipeline and/or the methods section for an article with the
appropriate references (akin to what fMRIprep already does).

In a similar way, FSL already outputs methods description for every
preprocessing or statistical analysis that can be used to write the methods
section of a paper as explained by Jeanette Mumford in this [video](https://www.youtube.com/watch?v=1SOIUVnTglM).

## Integration with BIDS and NIDM

The process of filling in an online checklist can be simplified
if the required information can be directly accessed
from the metadata in some of the existing standards for data and results like:

1.  the brain imaging data structure ([BIDS](http://bids.neuroimaging.io/)) used for that study,
1.  the [NIDM results](http://nidm.nidash.org/specs/nidm-results_130.html) of any mass-univariate analysis performed for this study.

**BIDS** is an emerging standard to organize neuroimaging data (MRI, fMRI,
EEG...) and its associated metadata regarding acquisition (like repetition time,
echo time, slice order...), experimental design (number of subjects, conditions,
stimulus onsets...).
If a data set is organized following the BIDS standard, it
is possible to query its content using
[pybids](https://github.com/bids-standard/pybids) or
[bids-matlab](https://github.com/bids-standard/bids-matlab) and even write part
of the method section relative to the acquisition using the `reports module` of those packages
(see for example [pybids reports](https://github.com/bids-standard/pybids/tree/master/bids/reports)).

**NIDM** results is a way to package mass-univariate fMRI results in a software independent way.
This way it can for example facilitate reading FSL results
through SPM or facilitate data sharing (like NIDM results is supported by the
data sharing platform [Neurovault](https://neurovault.org/) and this greatly
facilitate uploading your results there).
NIDM contains many metadata with a correspondence in the COBIDAS checklist
(see [here](https://static-content.springer.com/esm/art%3A10.1038%2Fsdata.2016.102/MediaObjects/41597_2016_BFsdata2016102_MOESM100_ESM.pdf)).

For BIDS and NIDM results, machine reading through a dataset organized as BIDS and NIDM results
could automatically fill part of the COBIDAS checklist.

Conversely it is possible to help users create some files that make up a BIDS dataset
by having them fill in part of the checklist.

An implementation of this, will most likely rely on the respective schema of
those resources:

-   [BIDS schema](https://github.com/bids-standard/bids-specification/tree/master/src/schema).
-   NIDM schema: **link missing**

<!-- TODO add NIDM schema link -->

## Integration with existing ontologies

To automate the creation certain aspects we could try to rely on some existing ontologies
that create list of term definitions to generate or enrich the list of response choices to some items.

Examples of this could rely on
[scicrunch](https://scicrunch.org/scicrunch/interlex/dashboard) and the
[NIDM-terms](https://scicrunch.org/nidm-terms) or the
[Research resource IDentifiers](https://scicrunch.org/resources).

## Link to pipeline-creating tools

Though more challenging, it could be imagined that pipeline-creating-tools like
([nipype](https://nipype.readthedocs.io/en/latest/),
[PORCUPINE](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006064),
[GIRAFFE](https://giraffe.tools/porcupine/TimVanMourik/GiraffePlayground/master))
could also generate json files to be used for method section generation.

## Facilitate data sharing

If the output created by the checklist app is accepted by neuroimaging databases
(e.g. [Neurovault](https://neurovault.org/)) as metadata input, this could
reduces friction for data sharing.
Users wouldn't have to fill several times the
same information: when pre-registering, when writing their methods, when
submitting to a journal (if it has a checklist of its own), when sharing data.
For example the metadata fields from
[neurovault](https://github.com/NeuroVault/NeuroVault/blob/master/scripts/metadata_neurovault.csv)
are already present in the COBIDAS checklist.

## Link to journal specific checklists

As some journals start having submission-checklists (e.g eLife,
[nature research journals](https://www.nature.com/nature-research/editorial-policies/reporting-standards)...),
filling in the a checklist only once could reduce 'the submission paperwork' by
writing part of the method section of the article AND generating the appropriate
submission-checklist for a given journal.

Reviewers could also use the website to systematically cross-check that all the
required methods and results information are present for a given paper.
A tool to compare different outputs from the web app could help editors visualize
agreement across reviewers' evaluation of a paper.

If the process is made sufficiently seamless, this could in return potentially incentivize more journals to adopt submission-checklists.
