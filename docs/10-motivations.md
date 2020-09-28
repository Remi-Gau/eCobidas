# Project motivations

## Improve transparency and reproducibility

In 2012, in a
[review of the methods and results reporting of more than 200 fMRI papers](https://www.ncbi.nlm.nih.gov/pubmed/22796459)
the author found that "*Although many journals urge authors to describe their
methods to a level of detail such that independent investigators can fully
reproduce their efforts, the results described here suggest that few studies
meet this criterion.*"

A few years ago, in order to improve reproducibility in f/MRI research, the
Committee on Best Practices in Data Analysis and Sharing
([COBIDAS](https://www.humanbrainmapping.org/i4a/pages/index.cfm?pageid=3728))
of OHBM released a [report](https://www.biorxiv.org/content/10.1101/054262v2) to
promote best practices for methods and results reporting. This was recently
followed by a [similar initiative for EEG and MEG](https://osf.io/a8dhx/).

Contrary to what the most optimistic people might have thought, these guidelines
do not seem to have been widely adopted and anecdotal evidence
([see that twitter poll and thread](https://treeverse.app/view/Xf3jfvIZ))
suggests that, even among people who know about the report, few of them use it
to write or review papers.

A [survey from ISMRM](https://ismrm.github.io/rrsg/QuestionnaireSummary/) seems
to suggest that the lack of method details is big problem in MRI research in
general but also that there seems to be little knowledge of the existence of the
COBIDAS report outside of some circles.

One possible reason for this might be the unwieldy nature of the report.
Anticipating this issue, the authors of the guidelines included a checklist
(Appendix D) that still ended up taking almost 30 of the 70 pages of the whole
document. Anyone who has used this checklist tends to agree that it is a great
resource but that it is a bit cumbersome to interpret and apply.

So the goal of this project is to facilitate the use of this checklist. But, if
done right, this could also in the long term enhance the adoption of emerging
neuroimaging standards (BIDS, fMRIprep, NIDM...), facilitate data sharing and
pre-registration, help with peer-review...

## Reduce inefficiencies

- lost time trying to figure out what: 
 - other authors did 
    - to compare our results
    - when reviewing papers
 - what we did 6 months ago

- we often have to report the same information
    - when writing a pre-registration
    - when curating our data
    - when writing our methods and results section 
    - when sharing data
