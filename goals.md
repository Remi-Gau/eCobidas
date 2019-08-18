# Goals

## Milestones (short term goals)

-   Discuss conceptual and structural details of the spreadsheet, COBIDAS-json file, branching logic of the checklist.

-   Create a spreadsheet where each item of the checklist has been properly atomized

-   Define use-case to simplify user experience

-   Identify high-priority items to report based on Carp 2012 to make sure users do better than 50% of the papers out there :heavy_check_mark: :smiley:

-   Create a proof of concept website that can:
    - given a template spreadsheet file generates a checklist to clicked through by users, :heavy_check_mark: :smiley:
    - outputs a populated COBIDAS-json file once the user is done, :heavy_check_mark: :smiley:
    - generate a method section using a populated COBIDAS-json file.

## Requirements

  The implementation of this project should remain flexible enough to:
  - accommodate the inclusion of new items in the checklist as new neuroimaging methods mature (e.g new multivariate analysis, high-resolution MRI...),
  - easily fork the project and convert it to create a checklist-website for a different field.

## Extensions (intermediate goals)

The process of filling in an online checklist can be simplified if of the required information can be directly accessed from the metadata in some of the existing standards for data and results curation like:
1. the brain imaging data structure ([BIDS](http://bids.neuroimaging.io/)) used for that study,
2. the [NIDM results](http://nidm.nidash.org/specs/nidm-results_130.html) of any mass-univariate analysis performed for this study.

BIDS is an emerging standard to organize neuroimaging data (MRI, fMRI, EEG...) and its associated metadata regarding acquisition (e.g repetition time, echo time, slice order...), experimental design (number of subjects, conditions, stimulus onsets...). This allows to automate methods section generation like is done by the `reports module` of [pybids](https://github.com/bids-standard/pybids/tree/master/bids/reports).

NIDM results is a way to present and package mass-univariate fMRI results in a software independent way. This way it can for example facilitate reading FSL results through SPM or facilitate data sharing (e.g NIDM results is supported by the data sharing platform neurovault and this greatly facilitate uploading your results there). NIDM contains many metadata with a correspondence in the COBIDAS checlist (see [here](https://media.nature.com/original/nature-assets/sdata/2016/sdata2016102/extref/sdata2016102-s1.pdf)).

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

2. facilitate systematic literature reviews and meta-analysis

3. facilitate data sharing

If the json file it creates is accepted by neuroimaging databases (e.g neurovault) as metadata input, this could reduces friction for data sharing. Users wouldn't have to fill several times the same information (when pre-registering, when writing their methods, when submitting to a journal if it has a checklist of its own, when sharing data). For example the metadata fields from [neurovault](https://github.com/NeuroVault/NeuroVault/blob/master/scripts/metadata_neurovault.csv) are already present in the COBIDAS checklist.

4. help make peer-review more objective

Reviewers could use the website to systematically cross-check that all the required methods and results information are present for a given paper. A tool to compare COBIDAS-json files could help editors visualize agreement across reviewers' json file.
