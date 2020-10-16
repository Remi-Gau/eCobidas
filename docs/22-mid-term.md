# Intermediate goals

Once we have a prototype for a checklist we want to optimize them to make that
they are comprehensive and cover all the items of the guidelines and to minimize
the amount of time the user has to interact with the checklist.

## Improve user-friendliness

In line with the idea of trying to minimize how much time the users have to
spend using the app, we want to pre-select response choices to some items
depending on the software users report having used in their analysis.

For example, if SPM was used to do slice timing correction, there is no reason
to ask users what type of interpolation was used as SPM does not give users the
possibility to choose that parameter. Finding out what are the choice options
for each item for the neuroimaging software used could help users navigate the
app faster.

Another potential way to improve users experience is to only expose users to
items that are relevant to them. For example, we want to make sure that the
items related "arterial spin labelling" are displayed only if the user mentioned
they used this technique in a previous section of the checklist.

### Improving the wording

The questions of the checklist must be as unambiguous as possible. This should
be improved through early user feedback.

## Extended checklists

Right now, several of the
[prototypes](https://github.com/Remi-Gau/eCobidas/tree/master/README.md#prototypes)
contains only a subset of all the questions from the reports they came from. For
example, the MRI checklist only contain the items corresponding to the metadata
of a collection of results uploaded on [Neurovault](https://neurovault.org/).

In the near future, we want to be able to extend those checklists so they
include **all** the items listed in their guidelines.

## Links to standardized pipelines

Data processed with some standardized pipelines (like
[fMRIprep](https://fmriprep.readthedocs.io/en/stable/citing.html)) could
facilitate filling in the checklist: ticking the box corresponding to that
pipeline would automatically populate all the relevant fields in the
COBIDAS-json file.

## Standardize terminology

Ensure that the across apps the same terminology is used by trying to rely on
the BIDS terminology with reference to other lexicons or ontology.
