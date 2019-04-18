# COBIDAS checklist

This repository is a first step in trying to turn the report published by the Committee on Best Practices in Data Analysis and Sharing (COBIDAS) of OHBM into a practical tool for improving methods and results reporting in neuroimaging.

This repository should be a place where:
1. issues and ideas around reaching this goal are discussed;
2. plans for how to reach this goal may be designed and implemented.

## How to reach us
[The github repository of this project can be found here](https://github.com/Remi-Gau/COBIDAS_chckls)

Come and join us on the `cobidas_checklist` channel at [![slack_brainhack_3](https://user-images.githubusercontent.com/6297454/47951457-5b37b780-df61-11e8-9d77-7b5a4c7af875.png)](https://brainhack-slack-invite.herokuapp.com/).

Otherwise you can open a new issue on the repository itself if there is something you would like to discuss directly here.

## Project Description
In 2012, in a [review of the methods and results reporting of more than 200 fMRI paper](https://www.ncbi.nlm.nih.gov/pubmed/22796459) the author found that "_Although many journals urge authors to describe their methods to a level of detail such that independent investigators can fully reproduce their efforts, the results described here suggest that few studies meet this criterion._"

In order to address this issue of replicability in f/MRI research, [COBIDAS](https://www.humanbrainmapping.org/i4a/pages/index.cfm?pageid=3728) released a [guidelines](https://www.biorxiv.org/content/10.1101/054262v2) for best practices in reporting of methods and results. This was soon followed by a [similar initiative for EEG and MEG](https://osf.io/a8dhx/).

Contrary to what the most optimistic people might have thought, these guidelines do not seem to have been widely adopted and anecdotal evidence ([see that twitter poll and thread](https://treeverse.app/view/Xf3jfvIZ)) suggests that, even among people who know about the report, few of them use it to write or review papers.

One possible reason for this might be the unwieldy nature of the report. Anticipating this issue, the authors of the guidelines included a checklist (Appendix D) that still ended up taking almost 30 of the 70 pages of the whole document. Anyone who has used this checklist tends to agree that it is a great resource but that it is a bit cumbersome to interpret and apply.

### Short term goal

**The short term goal of this project is to make the Appendix D checklist easier to use**.

One way to achieve this may be to turn the checklist into a website that users can click through and provide the information requested by COBIDAS.

Ideally this would generate a small text file (for example a json file) that summarizes the response provided for each item of the checklist.

This machine readable file could then be used to automatically generate part of the methods section of an article.

#### Extensions

The process of filling in an online checklist could be simplified if available metadata was drawn in from machine readable files created in the fulfilment of existing standards, for example:
1. the [Brain imaging data structure](http://bids.neuroimaging.io/)  used for that study (for example with respect to the data acquisition and experimental design).
2. the [NIDM results](http://nidm.nidash.org/specs/nidm-results_130.html) of any mass-univariate analysis performed for this study.

#### Further developments

Other off-shoot of this project could include developing toolboxes / packages / plug-ins for the main neuroimaging software (SPM, FSL, AFNI, Freesurfer) that would take a processing batch file as input (e.g matlabbatch.mat for SPM or design.fsf for FSL) and output json files that could be used on the proposed COBIDAS checklist website to automatically generate methods section (in a similar way to [fMRIprep](https://fmriprep.readthedocs.io/en/stable/citing.html))
