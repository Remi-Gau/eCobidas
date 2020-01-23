# Goals

## Imagined impact on the field of neuroimaging ("pie in the sky" goals)

This checklist could:

1. provide comprehensive descriptions of the analysis pipelines used in published papers, both human- and machine-readible (use the app to **document** pipelines)

2. facilitate pre-registration and registered reports (use the app to **create** pipelines)

3. facilitate systematic literature reviews and meta-analyses (use the app to **read** pipelines)

4. facilitate data sharing (use the app to **standardize** the report of information)

If the json file it creates is accepted by neuroimaging databases (e.g neurovault) as metadata input, this could reduces friction for data sharing. Users wouldn't have to fill several times the same information (when pre-registering, when writing their methods, when submitting to a journal if it has a checklist of its own, when sharing data). For example the metadata fields from [neurovault](https://github.com/NeuroVault/NeuroVault/blob/master/scripts/metadata_neurovault.csv) are already present in the COBIDAS checklist.

5. help make peer-review more objective (use the app to **check** pipelines)

Reviewers could use the website to systematically cross-check that all the required methods and results information are present for a given paper. A tool to compare COBIDAS-json files could help editors visualize agreement across reviewers' json file. For an example for human data published, see this paper by [Aczel et al. 2020](https://www.nature.com/articles/s41562-019-0772-6) and the respective [shinyapp](http://www.shinyapps.org/apps/TransparencyChecklist/).

## Requirements for the implementation

  The implementation of this project should remain flexible enough to:
  - accommodate the inclusion of new items in the checklist as new neuroimaging methods mature (e.g new multivariate analysis, high-resolution MRI...),
  - easily fork the project and convert it to create a checklist-website for a different field.


## Milestones (short term goals)

**The short term goal of this project is to create a website with a clickable checklist that, at the end, automatically generates most of the method section of a f/MRI or MEEG paper.**

### MRI COBIDAS

So far the short goals of the MRI app have been:

-   Create a proof of concept website that can:
    - given a template spreadsheet file generates a checklist to clicked through by users, :heavy_check_mark: :smiley:
    - outputs a populated JSON file once the user is done, :heavy_check_mark: :smiley:
    - generate a method section using this JSON file.

By working on those first step, a proof of concept app has been put together. There is now work to be done to extend what this app can do so we can have a first release that could be used for a typical fMRI study with:
-   a single functional task
-   one anatomical scan
-   using mass uni-variate analysis

To reach that first milestone we still need to work on the following isues:
-   Identify high-priority items that at least include those from [Carp 2012](https://www.ncbi.nlm.nih.gov/pubmed/22796459) to make sure users do better than 50% of the papers reported in this study
-   Create a version of the spreadsheet where each of those high priority items has been properly atomized (i.e it is only composed of a single question)
-   Identify ways in which the user experience can be improved, mostly by finding ways to minimize the time users have to spend using the app.
-   Identify defaults in the most common software packages (SPM, FSL, AFNI) to inform users about potential answers

### MEEG COBIDAS

The MRI version is currently ahead and the work done there can pave the way for the MEEG version. The MEEG version should have the same overall structure as the MRI version.
The MEEG version currently still awaits the final release of the MEEG COBIDAS guidelines (see the [preprint](https://osf.io/a8dhx/) and [webpage](https://cobidasmeeg.wordpress.com/)).

The main short term goals for the MEEG version are:

-   Identify overlaps between the MEEG and the f/MRI spreadsheet and harmonize both versions
-   Identify high-priority items in the checklist (similar to Carp 2012 for fMRI, e.g. [Luck & Gaspelin 2015](https://onlinelibrary.wiley.com/doi/full/10.1111/psyp.12639))
-   Create a version of the spreadsheet where each of those high priority items has been properly atomized (i.e it is only composed of a single question)
-   For each item:
  -  Give it an item name
  -  Create a specific unambiguous question
  -  Identify the response type expected (based on exemplary software)
      - Determine which softwares are considered in the examples
  -  Create a response choice list where needed
  -  Check if the item can be extracted from a BIDS data set


## Extensions (intermediate goals)

### Extended checklists
Right now, the [prototype](https://cobidas-checklist.herokuapp.com/) contains some of questions from the COBIDAS reports. 
In the near future, we want to be able to extend those checklists so they include **all** the items listed in the COBIDAS reports. Also, it will create human-readible method sections as outputs.

### Links with BIDS and NIDM
The process of filling in an online checklist can be simplified if of the required information can be directly accessed from the metadata in some of the existing standards for data and results curation like:
1. the brain imaging data structure ([BIDS](http://bids.neuroimaging.io/)) used for that study,
2. the [NIDM results](http://nidm.nidash.org/specs/nidm-results_130.html) of any mass-univariate analysis performed for this study.

**BIDS** is an emerging standard to organize neuroimaging data (MRI, fMRI, EEG...) and its associated metadata regarding acquisition (e.g repetition time, echo time, slice order...), experimental design (number of subjects, conditions, stimulus onsets...). This allows to automate methods section generation like is done by the `reports module` of [pybids](https://github.com/bids-standard/pybids/tree/master/bids/reports).

**NIDM** results is a way to present and package mass-univariate fMRI results in a software independent way. This way it can for example facilitate reading FSL results through SPM or facilitate data sharing (e.g NIDM results is supported by the data sharing platform neurovault and this greatly facilitate uploading your results there). NIDM contains many metadata with a correspondence in the COBIDAS checklist (see [here](https://media.nature.com/original/nature-assets/sdata/2016/sdata2016102/extref/sdata2016102-s1.pdf)).

For BIDS and NIDM results, machine reading through a data set organized as BIDS and and NIDM results could automatically fill part of the COBIDAS checklist.

### Links to standarized pipelines (fMRIprep)
In a similar way, data processed with some standardized pipelines (e.g fMRIprep) could facilitate filling in the checklist: ticking the box corresponding to that pipeline would automatically populate all the relevant fields in the COBIDAS-json file.

### Automatic information extraction from source data (DICOM)
One can also imagine that pointing to a folder containing source MRI data (e.g DICOM) could allow the extraction of several of the information required by the COBIDAS checklist.

## Further developments (long term goals)

### Link to main neuroimaging software

Another potential way to improve users experience is to only expose users to items or response choices that are relevant to them, i.e. options that users can actively change. For example, if SPM was used to do slice timing correction, there is no reason to ask users what type of interpolation was used as SPM does not give users the possibility to choose that parameter. Finding out what are the choice options for each item for the neuroimaging software used could help users navigate the app.

A side branch of this project includes developing plugins for the main neuroimaging software toolboxes (SPM, FSL, AFNI). Such a plugin would receive processing batch files as input (e.g matlabbatch.mat for SPM or design.fsf for FSL) and would create output files (e.g. in json format) readable by the COBIDAS checklist website, which in turn would be able to display the neuroimage processing pipeline and/or generate part of the methods section for an article with the appropriate references (in a similar way to [fMRIprep](https://fmriprep.readthedocs.io/en/stable/citing.html)).

In a similar way, FSL already outputs methods description for every preprocessing or statistical analysis that can be used to write the methods section of a paper as explained by Jeanette Mumford in this [video](https://www.youtube.com/watch?v=1SOIUVnTglM).

### Link to pipeline-creating tools

Though more challenging, it could be imagined that pipeline-creating-tools like ([nipype](https://nipype.readthedocs.io/en/latest/), [PORCUPINE](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006064), [GIRAFFE](https://giraffe.tools/porcupine/TimVanMourik/GiraffePlayground/master)) could also generate COBIDAS-json file.

### Link to journal specific checklists
As some journals start having submission-checklists (e.g elife, [nature research journals](https://www.nature.com/nature-research/editorial-policies/reporting-standards)...), filling in the COBIDAS checklist once could reduce 'the submission paperwork' by writing part of the method section of the article AND generating the appropriate submission-checklist for a given journal.

If the process is made sufficiently seamless, this could in return potentially incentivize more journals to adopt submission-checklists.

### Link to neurolex
Try to see if list of choices presented to users on some items or if the terminology used by the checklist in general can be linked to the neurolex "ontology".
