O# Improving the COBIDAS checklist for better neuroimaging methods and results reporting

Remi Gau ([ORCID](https://orcid.org/0000-0002-1535-9767))

## Project Description
In 2012, in his review of the methods and results reporting of more than 200 fMRI papers, [Joshua Carp wrote](https://www.ncbi.nlm.nih.gov/pubmed/22796459): "_Although many journals urge authors to describe their methods to a level of detail such that independent investigators can fully reproduce their efforts, the results described here suggest that few studies meet this criterion._"

A few years ago, in order to improve the situation with respect to [reproducibility](https://github.com/ohbm/hackathon2019/blob/master/Tutorial_Resources.md#reproducible-neuroimaging-tools) in f/MRI research, the Committee on Best Practices in Data Analysis and Sharing ([COBIDAS](https://www.humanbrainmapping.org/i4a/pages/index.cfm?pageid=3728)) of OHBM released a [report](https://www.biorxiv.org/content/10.1101/054262v2) to promote best practices for methods and results reporting. This was recently followed by a [similar initiative for EEG and MEG](https://osf.io/a8dhx/).

So far these guidelines do not seem to have been widely adopted and anecdotal evidence ([see that twitter poll and thread](https://treeverse.app/view/Xf3jfvIZ)) suggests that even among people who know about the report few of them use it to write or review papers. One likely reason for this might be the unwieldy nature of the report. Anyone who has used this checklist tends to agree that it is a great resource but that it is a bit cumbersome to interpret and apply.

So the short term goal of this project is to facilitate the use of this checklist. But, if done right, this could also in the long term enhance the adoption of emerging neuroimaging standards ([the Brain imaging data structure](https://github.com/ohbm/hackathon2019/blob/master/Tutorial_Resources.md#the-brain-imaging-data-structure-bids), fMRIprep, NIDM...), facilitate data sharing and pre-registration, help with peer-review...

### Short term goal

**The short term goal of this project is to make the COBIDAS report easier to use: we want to create a website with a clickable checklist that generates a json file at the end.**

By turning the checklist into a website users could more rapidly click through it and provide more of the information requested by the COBIDAS report. This would generate a small text file (a json file) that summarizes what option was chosen for each item of the checklist. This machine readable file could then be used to automatically generate part of the methods section of an article.

Other potential goals (e.g. interaction with BIDS and NIDM, further integration with main neuroimaging softwares...) and potential applications (improving data-sharing and peer-review) of this project are described in this [repository](https://github.com/Remi-Gau/COBIDAS_chckls).


## Skills required to participate

One or more of those:

- To be enthusiastic about reproducibility
- Familiarity with the COBIDAS report for f/MRI, MEEG,
- To know something about web design,
- Familiarity with one or more of the main neuroimaging software for [fMRI](https://github.com/ohbm/hackathon2019/blob/master/Tutorial_Resources.md#neuroimaging) (SPM, FSL...) or for [M/EEG](https://github.com/ohbm/hackathon2019/blob/master/Tutorial_Resources.md#main-eeg-and-meg-softwares) (Fieldtrip, EEGlab...)


## Milestones

- Discuss conceptual and structural details of the COBIDAS-json file.

- Create a template of the COBIDAS-json file

- Create a proof of concept website that can:
  - given a template COBIDAS-json file generates a checklist to clicked through by users,
  - outputs a populated COBIDAS-json file once the user is done,
  - generate a method section using a populated COBIDAS-json file.


## Preparation material

Jeanette Mumford has a [30 min video](https://www.youtube.com/watch?v=bsM4KowO5Vc&t=175s) on her youtube channel explaining the background behind the COBIDAS report and giving a run through of the checklist.

The COBIDAS report:
- [for MRI and fMRI](https://www.biorxiv.org/content/10.1101/054262v2)
- [for EEG and MEG](https://osf.io/a8dhx/)

A [spreadsheet version](https://osf.io/qkb9t/) of the COBIDAS checklist (thanks to [Cass](https://github.com/cassgvp)!!!)

[The secret lives of experiments: methods reporting in the fMRI literature](https://www.ncbi.nlm.nih.gov/pubmed/22796459)

[A manifesto for reproducible science](https://www.nature.com/articles/s41562-016-0021)

## GitHub repo

[The github repository of this project can be found here](https://github.com/Remi-Gau/COBIDAS_chckls)


## Communication

Come and join us on the `cobidas_checklist` channel at [![slack_brainhack_3](https://user-images.githubusercontent.com/6297454/47951457-5b37b780-df61-11e8-9d77-7b5a4c7af875.png)](https://brainhack-slack-invite.herokuapp.com/).
