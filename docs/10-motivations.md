# Project motivations

## Improve transparency and reproducibility

In 2012, in a
[review of the methods](https://www.ncbi.nlm.nih.gov/pubmed/22796459) of more
than 200 fMRI papers, the author found that "_Although many journals urge
authors to describe their methods to a level of detail such that independent
investigators can fully reproduce their efforts, the results described here
suggest that few studies meet this criterion._"

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
Anticipating this issue, the authors of the guidelines included a checklist that
still ended up taking almost 30 of the 70 pages of the whole document. Anyone
who has used this checklist tends to agree that it is a great resource but that
it is a bit cumbersome to interpret and apply.

So the goal of this project is to facilitate the use of this checklist and of
similar guidelines.

## Reduce inefficiencies

Currently, the research workflow around methods reporting has us do the same
thing several times (very often manually) which leads to inefficiencies and
multiplies the chances for human errors like forgetting to report some
parameters or mis-reporting it.

For example, a researcher would have to write or rewrite some aspects of the
methods used when

1.  when preparing a pre-registration describing the planned study
1.  during the data curation process that usually involves adding metadata
    elements that relate to the details of the data acquisition,
1.  when actually working the methods and results section where we have to back
    and forth to the code we used to run the experiment and to the dataset to
    make sure important details are accurately reported,
1.  when sharing raw or derived data which also usually involves adding a
    minimum of methods-related metadata if the shared data is to be meaningfully
    reusable.

Another source of inefficiency is the time lost trying to figure out:

-   what the authors of a paper actually did
    -   when we would like to compare our results to theirs
    -   when reviewing papers
-   what we actually did 6 months ago but forgot to make a note of it.

So a potential side effect of using a checklist to systematically capture how
data was acquired and analyzed would therefore be to make us more efficient.
Having filled in a checklist once to generate a small set of files that capture
the vast majority of our acquisition and analysis pipeline, we could easily
share those files with our data, when submitting a paper or to generate a method
section automatically.
