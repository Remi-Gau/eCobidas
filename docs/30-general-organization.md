# General organization

<!-- TOC -->

-   [General organization](#general-organization)
    -   [Spreadsheet work](#spreadsheet-work)
        -   [Spreadsheet content and organization](#spreadsheet-content-and-organization)
    -   [How is the Repronim schema organized](#how-is-the-repronim-schema-organized)

<!-- /TOC -->

<!-- TODO
- mention OSF
- mention Zotero
 -->

<!-- ```
.
├── activities
├── communication
├── docs
├── inputs
├── node_modules
├── protocols
├── response_options
├── schema
├── scripts
└── tests
``` -->

There are 3 repositories behind this checklist:

1.  this
    [COBIDAS_chckls repository](https://github.com/Remi-Gau/COBIDAS_chckls/)
    where you are currently reading this. It contains:
    -   the [neurovault spreadsheet](./xlsx/metadata_neurovault.csv)
    -   the python [script](./python/create_ecobidas_schema.py) to turn that
        spreadsheet into a Repronim schema (basically a bunch hierarchically
        organized json files that link to each other).

2. Reproschema

3. the ui

  the [cobidas-ui repository](https://github.com/Remi-Gau/cobidas-ui) that
    does the actual rendering of the checklist app by reading the schema hosted
    by the previous repository. There is a general explanation of how the app
    works in this [issue](https://github.com/ReproNim/schema-ui/issues/4). The
    prototype app for this checklist can be, for now, found
    [here](https://cobidas-checklist.herokuapp.com/)

ohbm/cobidas repo

add info on reproschema template about what to modify

## Spreadsheet content and organization

See the dedicated [document](./spreadsheet-content.md)

## How is the Reproschema organized

<!-- TODO link to reproschema doc -->

https://www.repronim.org/reproschema/

https://www.repronim.org/reproschema/98_FAQ/ 

https://github.com/ReproNim/reproschema/pull/399

https://github.com/Remi-Gau/reproschema/tree/remi-documentation/docs

The first step to create the checklist involves taking a spreadsheet that
contains all the items and turning that into a representation that can
efficiently link the metadata about each item to the data imputed by the user.
Basically it means turning your 'dumb' spreadsheet into an equivalent but
'smarter' representation of it: in this case a bunch hierarchically organized
json files that link to each other.

In terms of choice of representation we are using the
[reproschema](https://github.com/ReproNim/reproschema) initiative from
[ReproNim](http://www.repronim.org/) to do this. On top of the inherent
[advantages](https://github.com/ReproNim/reproschema#30-advantages-of-current-representation)
of this schema representation:

-   its use simplifies the rendering of the checklist by using the
    [schema-ui](https://github.com/ReproNim/schema-ui) made for it,
-   this representation allows specification of user interface option that can
    simplify the user experience: it allows us to specify a `branching logic`
    that will prevent users to be presented with items that are not relevant to
    them (e.g answer PET related when they have only run an fMRI study).

The repronim schema is organized in a hierarchical manner with 3 levels.

1.  The lowest level is the `item level` where there is one question for each
    item with an expected format for the user interface: is this yes / no
    question (boolean), a multiple choice, a float or an integer...
2.  The second level is the `activity level` that contains a set of items. In
    the original repronim project this would constitute usually a questionnaire:
    like all the items of the Edinburgh handedness inventory would constitute
    one activity. In the COBIDAS case, it seems that we will most likely use
    this level to define some 'big' section of a method section (e.g.
    preprocessing, design, participants...)
3.  The highest level is the `activity_set` or protocol level that originally
    define a set of activities to be included in a given study. At the moment
    this level is underused in the COBIDAS checklist but could be used to define
    activity sets for different use case: fMRI, MEEG, pre-registration...

So far we have a [script](./python/create_ecobidas_schema.py) to turn the
neurovault [list of required inputs](./xlsx/metadata_neurovault.csv) into a
schema that can then be render with the schema-ui.
