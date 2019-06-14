# COBIDAS checklist

This repository host the work turning the report published by the Committee on Best Practices in Data Analysis and Sharing (COBIDAS) of the organization for human brain mapping (OHBM) into a practical tool for improving methods and results reporting in neuroimaging.

This repository should be a place where:
1. issues and ideas around reaching this goal are discussed;
2. plans for how to reach this goal may be designed and implemented.


## How to reach us

If you want to kept posted about the progress of the project, you can join our [google group](https://groups.google.com/d/forum/cobidas-checklist).

From more frequent updates and behind the scenes, come and join us on the `cobidas_checklist` channel on the brainhack mattermost.

<a href="https://mattermost.brainhack.org/brainhack/channels/cobidas_checklist"><img src="http://www.mattermost.org/wp-content/uploads/2016/03/logoHorizontal.png" width=100px /> Join our channel </a>

Otherwise you can open a new issue on the repository itself if there is something you would like to discuss directly here.


## Why this project

Poor methods and results description hinders the reproducibility and the replicability of research. It also makes it hard to compare new and old results and generally increases inefficiency in the research process. This project is built on the hope that improving methods and results reporting could improve neuroimaging research.

See [here](why_this_project.md) to for more background information.



## Short term goal

**The short term goal of this project is to make the COBIDAS report easier to use: we want to create a website with a clickable checklist that generates a json file at the end.**

By turning the checklist into a website users could more rapidly click through it and provide more of the information requested by the COBIDAS report. This would generate a small text file (a json file) that summarizes what option was chosen for each item of the checklist. This machine readable file could then be used to automatically generate part of the methods section of an article.

### Milestones

- Discuss conceptual and structural details of the COBIDAS-json file.

- Create a template of the COBIDAS-json file

- Create a proof of concept website that can:
  - given a template COBIDAS-json file generates a checklist to clicked through by users,
  - outputs a populated COBIDAS-json file once the user is done,
  - generate a method section using a populated COBIDAS-json file.

### Requirements

  The implementation of this project should remain flexible enough to:
  - accommodate the inclusion of new items in the checklist as new neuroimaging methods mature (e.g new multivariate analysis, high-resolution MRI...),
  - easily fork the project and convert it to create a checklist-website for a different field. In practice, this will involve a deployment through a container technology like [docker](https://github.com/ohbm/hackathon2019/blob/master/Tutorial_Resources.md#containers).

### Extensions (intermediate goals)

The process of filling in an online checklist can be simplified if of the required information can be directly accessed from the metadata in some of the existing standards for data and results curation like:
1. the brain imaging data structure ([BIDS](http://bids.neuroimaging.io/)) used for that study,
2. the [NIDM results](http://nidm.nidash.org/specs/nidm-results_130.html) of any mass-univariate analysis performed for this study.

BIDS is an emerging standard to organize neuroimaging data (MRI, fMRI, EEG...) and its associated metadata regarding acquisition (e.g repetition time, echo time, slice order...), experimental design (number of subjects, conditions, stimulus onsets...). This allows to automate methods section generation like is done by the `reports module` of [pybids](https://github.com/bids-standard/pybids/tree/master/bids/reports).

NIDM results is a way to present and package mass-univariate fMRI results in a software independent way. This way it can for example facilitate reading FSL results through SPM or facilitate data sharing (e.g NIDM results is supported by the data sharing platform neurovault and this greatly facilitate uploading your results there). NIDM contains many metadata with a correspondance in the COBIDAS checlist (see [here](https://media.nature.com/original/nature-assets/sdata/2016/sdata2016102/extref/sdata2016102-s1.pdf)).

For BIDS and NIDM results, machine reading through a data set organized as BIDS and and NIDM results could automatically fill part of the COBIDAS checklist.

In a similar way, data processed with some standardized pipelines (e.g fMRIprep) could facilitate filling in the checklist: ticking the box corresponding to that pipeline would automatically populate all the relevant fields in the COBIDAS-json file.

One can also imagine that pointing to a folder containing source MRI data (e.g DICOM) could allow the extraction of several of the information required by the COBIDAS checlist.


## Further developments (long term goals)

### Link to main neuroimaging software

A side branch of this project includes developing plugins for the main neuroimaging software toolboxes (SPM, FSL, AFNI). Such a plugin would receive processing batch files as input (e.g matlabbatch.mat for SPM or design.fsf for FSL) and would create output files (e.g. in json format) readable by the COBIDAS checklist website, which in turn would be able to display the neuroimage processing pipeline and/or generate part of the methods section for an article with the appropriate references (in a similar way to [fMRIprep](https://fmriprep.readthedocs.io/en/stable/citing.html)).

In a similar way, FSL already outputs methods description for every preprocessing or statistical analysis that can be used to write the methods section of a paper as explained by Jeanette Mumford in this [video](https://www.youtube.com/watch?v=1SOIUVnTglM).

### Link to processing pipelines

Though more challenging, it could be imagined that pipeline-creating-tools like ([nipype](https://nipype.readthedocs.io/en/latest/), [PORCUPINE](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006064), [GIRAFFE](https://giraffe.tools/porcupine/TimVanMourik/GiraffePlayground/master)) could also generate COBIDAS-json file.

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

A [spreadsheet version](https://osf.io/qkb9t/) of the COBIDAS checklist (thanks to [Cass](https://github.com/cassgvp)!!!)

More ideas about this project are being added to this [google slide document](https://docs.google.com/presentation/d/17VOSLJQq6NpkCOFPR4iyEJngamugIqAfNBru0ohJbMo/edit?usp=sharing)
