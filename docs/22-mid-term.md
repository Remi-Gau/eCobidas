# Intermediate goals

## Extended checklists

Right now, the [prototype](https://ohbm.github.io/cobidas/#/**) contains only
some of questions from the COBIDAS reports: those that correspond to the
metadata of a collection of statistical maps uploaded on Neurovault. In the near
future, we want to be able to extend those checklists so they include **all**
the items listed in the COBIDAS reports. Also, it will create human-readible
method sections as outputs.

## Links with BIDS and NIDM

The process of filling in an online checklist can be simplified if of the
required information can be directly accessed from the metadata in some of the
existing standards for data and results curation like:

1. the brain imaging data structure ([BIDS](http://bids.neuroimaging.io/)) used
   for that study,

1. the [NIDM results](http://nidm.nidash.org/specs/nidm-results_130.html) of any
   mass-univariate analysis performed for this study.

**BIDS** is an emerging standard to organize neuroimaging data (MRI, fMRI,
EEG...) and its associated metadata regarding acquisition (e.g repetition time,
echo time, slice order...), experimental design (number of subjects, conditions,
stimulus onsets...). This allows to automate methods section generation like is
done by the `reports module` of
[pybids](https://github.com/bids-standard/pybids/tree/master/bids/reports).

**NIDM** results is a way to present and package mass-univariate fMRI results in
a software independent way. This way it can for example facilitate reading FSL
results through SPM or facilitate data sharing (e.g NIDM results is supported by
the data sharing platform neurovault and this greatly facilitate uploading your
results there). NIDM contains many metadata with a correspondence in the COBIDAS
checklist (see
[here](https://media.nature.com/original/nature-assets/sdata/2016/sdata2016102/extref/sdata2016102-s1.pdf)).

For BIDS and NIDM results, machine reading through a data set organized as BIDS
and and NIDM results could automatically fill part of the COBIDAS checklist.

## Links to standarized pipelines (fMRIprep)

In a similar way, data processed with some standardized pipelines (e.g fMRIprep)
could facilitate filling in the checklist: ticking the box corresponding to that
pipeline would automatically populate all the relevant fields in the
COBIDAS-json file.

## Automatic information extraction from source data (DICOM)

One can also imagine that pointing to a folder containing source MRI data (e.g
DICOM) could allow the extraction of several of the information required by the
COBIDAS checklist.
