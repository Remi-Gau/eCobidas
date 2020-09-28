# Long term goals

## Link to main neuroimaging software

Another potential way to improve users experience is to only expose users to
items or response choices that are relevant to them, i.e. options that users can
actively change. For example, if SPM was used to do slice timing correction,
there is no reason to ask users what type of interpolation was used as SPM does
not give users the possibility to choose that parameter. Finding out what are
the choice options for each item for the neuroimaging software used could help
users navigate the app.

A side branch of this project includes developing plugins for the main
neuroimaging software toolboxes (SPM, FSL, AFNI). Such a plugin would receive
processing batch files as input (e.g matlabbatch.mat for SPM or design.fsf for
FSL) and would create output files (e.g. in json format) readable by the COBIDAS
checklist website, which in turn would be able to display the neuroimage
processing pipeline and/or generate part of the methods section for an article
with the appropriate references (in a similar way to
[fMRIprep](https://fmriprep.readthedocs.io/en/stable/citing.html)).

In a similar way, FSL already outputs methods description for every
preprocessing or statistical analysis that can be used to write the methods
section of a paper as explained by Jeanette Mumford in this
[video](https://www.youtube.com/watch?v=1SOIUVnTglM).

## Link to pipeline-creating tools

Though more challenging, it could be imagined that pipeline-creating-tools like
([nipype](https://nipype.readthedocs.io/en/latest/),
[PORCUPINE](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006064),
[GIRAFFE](https://giraffe.tools/porcupine/TimVanMourik/GiraffePlayground/master))
could also generate COBIDAS-json file.

## Link to journal specific checklists

As some journals start having submission-checklists (e.g elife,
[nature research journals](https://www.nature.com/nature-research/editorial-policies/reporting-standards)...),
filling in the COBIDAS checklist once could reduce 'the submission paperwork' by
writing part of the method section of the article AND generating the appropriate
submission-checklist for a given journal.

If the process is made sufficiently seamless, this could in return potentially
incentivize more journals to adopt submission-checklists.

## Link to neurolex

Try to see if list of choices presented to users on some items or if the
terminology used by the checklist in general can be linked to the neurolex
"ontology".

## Potential applications ("pie in the sky" goals)

If the json file it creates is accepted by neuroimaging databases (e.g.
neurovault) as metadata input, this could reduces friction for data sharing.
Users wouldn't have to fill several times the same information (when
pre-registering, when writing their methods, when submitting to a journal if it
has a checklist of its own, when sharing data). For example the metadata fields
from
[neurovault](https://github.com/NeuroVault/NeuroVault/blob/master/scripts/metadata_neurovault.csv)
are already present in the COBIDAS checklist.

Reviewers could use the website to systematically cross-check that all the
required methods and results information are present for a given paper. A tool
to compare COBIDAS-json files could help editors visualize agreement across
reviewers' json file.
