# COBIDAS checklist

This repository is a first step in trying to turn the report published by the Committee on Best Practices in Data Analysis and Sharing (COBIDAS) of OHBM into an easy to use checklist to improve methods and results reporting in neuroimaging.

This should a place where:
1. issues and ideas around reaching that goal are discussed,
2. plans on how to get to this goal are designed and implemented.


## How to reach us

[The github repository of this project can be found here](https://github.com/Remi-Gau/COBIDAS_chckls)

Come and join us at on the `cobidas_checklist` channel on the [![slack_brainhack_3](https://user-images.githubusercontent.com/6297454/47951457-5b37b780-df61-11e8-9d77-7b5a4c7af875.png)](https://brainhack-slack-invite.herokuapp.com/).

Otherwise you can open a new issue if there is something you would like to discuss directly here.


## Project Description

In 2012, in a [review of the methods and results reporting of more than 200 fMRI paper](https://www.ncbi.nlm.nih.gov/pubmed/22796459) the author found that "_Although many journals urge authors to describe their methods to a level of detail such that independent investigators can fully reproduce their efforts, the results described here suggest that few studies meet this criterion._"

A few years ago, in order to improve reproducibility in f/MRI research, the Committee on Best Practices in Data Analysis and Sharing ([COBIDAS](https://www.humanbrainmapping.org/i4a/pages/index.cfm?pageid=3728)) of OHBM released a [report](https://www.biorxiv.org/content/10.1101/054262v2) to promote best practices for methods and results reporting. This was recently followed by a [similar initiative for EEG and MEG](https://osf.io/a8dhx/).

Contrary to what the most optimistic people might have thought, these guidelines do not seem to have been widely adopted and anecdotal evidence ([see that twitter poll and thread](https://treeverse.app/view/Xf3jfvIZ)) suggests that, even among people who know about the report, few of them use it to write or review papers.

One possible reason for this might have the unwieldy nature of the report. Anticipating on this issue, the authors of the report had included a checklist that still ended up taking almost 30 of the 70 pages of the whole document. Anyone who has used this checklist tends to agree that it is a great resource but that it is a bit cumbersome to use.

So the short term goal of this project is to facilitate the use of this checklist. But, if done right, this could also in the long term enhance the adoption of emerging neuroimaging standards (BIDS, fMRIprep, NIDM...), facilitate data sharing and pre-registration, help with peer-review...


## Short term goal

**The short term goal of this project is to make this checklist easier to use**.

One way would be to turn it into a website that people can simply click their way through.

Ideally this would generate a small text file (for example a json file) that summarizes what option was chosen for each item of the checklist.

This machine readable file could then be used to automatically generate part of the methods section of an article.

### Extensions (intermediate goals)

Filling in that checklist could still be long and tedious so a way to facilitate this further would be read as much metadata as possible from existing standards like:
1. the [Brain imaging data structure](http://bids.neuroimaging.io/)  used for that study (for example with respect to the data acquisition and experimental design).
2. the [NIDM results](http://nidm.nidash.org/specs/nidm-results_130.html) of any mass-univariate analysis performed for this study.

In a similar way, data processed with some standardized pipelines (e.g fMRIprep) could facilitate filling in the checklist: ticking the box corresponding to that pipeline would automatically populate all the relevant fields.

### Requirements

The implementation of this project should remain flexible enough to:
- accommodate the inclusion of new items in the checklist as new neuroimaging methods mature (e.g new multivariate analysis, high-resolution fMRI...),
- easily fork the project and convert it to create a checklist-website for a different field.


## Further developments (long term goals)

### Link to main neuroimaging software

Other off-shoot of this project could include developing toolboxes / packages / plug-ins for the main neuroimaging software (SPM, FSL, AFNI, Freesurfer) that would take some processing batch file as input (e.g matlabbatch.mat for SPM) and would output json files that could be used on the COBIDAS checklist website to automatically generate methods section (in a similar way to [what fMRIprep does](https://fmriprep.readthedocs.io/en/stable/citing.html))

### Link to processing pipelines

Though more challenging, it could be imagined that pipeline-creating-tools like (nipype, PORCUPINE, GIRAFFE) could also generate COBIDAS-json file.

### Link to journal specific checklists
As some journals start having submission-checklists (e.g elife, nature communications...), filling in the COBIDAS checklist once could reduce 'the submission paperwork' by writing part of the method section of the article AND generating the appropriate submission-checklist for a given journal.

If the process is made sufficiently seamless, this could in return potentially incentivize more journals to adopt submission-checklists.


## Potential applications ("pie in the sky" goals)

This checklist could:

1. facilitate pre-registration and registered reports

2. facilitate data sharing

If the json file it creates is accepted by neuroimaging databases (e.g neurovault) as metadata input, this could reduces friction for data sharing. Users wouldn't have to fill several times the same information (when pre-registering, when writing their methods, when submitting to a journal if it has a checklist of its own, when sharing data). For example the metadata fields from [neurovault](https://github.com/NeuroVault/NeuroVault/blob/master/scripts/metadata_neurovault.csv) are already present in the COBIDAS checklist.

3. help make peer-review more objective

Reviewers could use the website to systematically cross-check that all the required methods and results information are present for a given paper. A tool to compare COBIDAS-json files could help editors visualize agreement across reviewers' json file.


## References

Jeanette Mumford has a [30 min video](https://www.youtube.com/watch?v=bsM4KowO5Vc&t=175s) explaining the background behind the COBIDAS report and giving a run through of the checklist.

The COBIDAS report:
- [for MRI and fMRI](https://www.biorxiv.org/content/10.1101/054262v2)
- [for EEG and MEG](https://osf.io/a8dhx/)

A [spreadsheet version](https://osf.io/qkb9t/) of the COBIDAS checklist (thanks to [Cass]!!!(https://github.com/cassgvp))

More ideas about this project are being added to this [google slide document](https://docs.google.com/presentation/d/17VOSLJQq6NpkCOFPR4iyEJngamugIqAfNBru0ohJbMo/edit?usp=sharing)
