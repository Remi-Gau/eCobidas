# Spreadsheet content

The spreadsheet aim to have one checklist item (one question) per row. In general it is recommended to NOT hide rows but instead to filter using some of the columns.

The MRI spreadsheet has some conditional formatting implemented so some cells will appear red when there is an error to be fixed. Some items that require more work might be manually highlighted in orange.

Here follows a description of the columns content. If some do not appear it is possible that they have been hidden by someone else. You will simply have to click on the double black arrow at the limit between columns to display them back.

![ ](img/show_hidden_columns.png)


## Referencing
The first few columns are only there to try in the future goal to create unique code identifier for each item.

| Apdx | Act | A1 | A2 | A3 | A4 | A5 | Ref1 | D | Reference |
|------|-----|----|----|----|----|----|------|---|-----------|


**This is low priority at the moment so those columns are hidden most of the time.**


## Filtering
The following columns can be used to filter which item to display.

| include_item |	neurovault_or_carp | mandatory |
|-|-|-|
| items that include items from `neurovault_or_carp` and some more | items that have their counterpart in the neurovault metadata list and/or that were surveyeed by Carp in 2012 |  items labelled as mandatory in the original COBIDAS report |

{>>Some of the choices for the items to include have been made in pretty arbitrary and one sided manner. This should be discussed further before moving on.<<}


## Schema activity name

| activity_name                                                                      |
|------------------------------------------------------------------------------------|
| This corresponds to the main section headings found in the original COBIDAS report |

{>>This might need some discussion too: it is possible that we might gain from splitting some of those into smaller sub-sections.<<}


## Item name

The `aspect` column allow for a human readable atomization of each section into items that are organize in a hierarchical fashion.

For example see below

| aspect_1        | aspect_2                                | aspect_3                     | aspect_4          | aspect_5 |
|-----------------|-----------------------------------------|------------------------------|-------------------|----------|
| MRI acquisition | Imaging type                            | partial fourrier scheme      |                   |          |
| MRI acquisition | Essential sequence & imaging parameters | All acquisitions             | voxel dimension   |          |
| MRI acquisition | Essential sequence & imaging parameters | Functional MRI               | number of volumes |          |
| MRI acquisition | Essential sequence & imaging parameters | Inversion recovery sequences | Inversion time    |          |
| MRI acquisition | Essential sequence & imaging parameters | Imaging parameters           | field of view     |          |
| MRI acquisition | Essential sequence & imaging parameters | Slice timing                 |                   |          |


Those columns are then used to create each item name.

| aspect_1 | aspect_2 | aspect_3 | aspect_4 | aspect_5 | item_name                                                      | item_name_duplicate                                                                                                                                                  |
|----------|----------|----------|----------|----------|----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|          |          |          |          |          | is determined by the content of the right most "aspect" column | each item_name must be unique in the entire column so there is a formula to double that there is no additional occurrence of that item name in the rest of the column |


## Question	and details

| question	| details |
| - | - |
| Each line must correspond to one checklist item that must have only one unambiguous question. Any item that opens the possibility of a response "if A was used then list the parameters B, C, D" must be broken down (atomize) into several items / questions: "1. Was A used? 2. If so what parameter was used for B? 3. What parameter was used for C? ...""  | Some questions might require some additional information to be understandable by all users, so any extra information to be displayed to the users should be put the detail column - it is still unclear at this moment how this will be displayed to the users  |


## Format

The type of answer expected must specified for each item.

- char: a text answer is expected
- boolean: a yes / no answer is expected
- float
- int : an integer is expected
- choice : the user must choose one answer from a list. The last option is always other and opens up the possibility to give a text answer
- multiple choice : several options can be chosen from the list

| format               | choice_levels                                             |
|----------------------|-----------------------------------------------------------|
| format for this item | list of choices in case of `choice` and `multiple choice` |


## Visibility and branching logic

We list the conditions that have to be fulfilled for each item to be displayed to the user. By default an item will be displayed (visibility = 1) or will only be shown if a specific answer has been given to a previous item.

If only an item_name is listed then this means that a positive answer must have been given to the question corresponding to that item name. Otherwise a specific choice must have been made on a previous question.

| visibility |
|------------|
|            |


## Default option

Later on, it will be useful to know either if some of the most commonly used software either have
- a "default" for some COBIDAS items (ideally this one should be the one at the top of the choice list when the user has specified their software).
- a more restricted list of choices for some items.

The limit case of the second case is where a software only has one option: e.g SPM only allows 6 degrees of freedom with a set cost function for realignment so there is no reason to ask the user for those info if they have done the realignment with SPM.

This could significantly speed things up for users

| SPM defaults | FSL defaults | AFNI defaults |
|--------------|--------------|---------------|
|   |   |   |

**This is low priority at the moment so those columns are hidden most of the time.**


## Import from other sources
| BIDS_status |	BIDS_source	 | BIDS_source_field	| NIDMs_results_status | neurovault |
|-|-|-|-|-|-|
| 0: does not exist in BIDS ; 1: exist in BIDS and can be extracted ; 2: could be included in BIDS ; 3: unknown |   |   |   |   |   |

List if the different items can be found (and where) in
- a BIDS data set
- an NIDM results package
- a neurovault collection

**This is low priority at the moment so those columns are hidden most of the time.**


## Comparison to Carp 2012
| in_Carp2012	| % of studies that informed it	| % of studies that informed it (structural)|
|-|-| - |
| item name used in Carp 2012  | If the number is bold, it means that it was approximately extracted from one of the figures of Carp2012 (because it was not reported in the text of the article)   | Same but for the structural data  |

This is for future reference: it lists the percentage of studies that reported each item according to Carp 2012. This could help figure out in which order items should be presented to users (e.g most reported items first and go down the priority list).

**This could prove useful later but is low priority at the moment so those columns are hidden most of the time.**


## Meta analysis use case
| use_case_meta-analysis	| meta-analysis_comment |
|-|-|
|   |   |

Where we will reference which item are more important when using the checklist to evaluate studies to use for a  meta-analysis.

**This is low priority at the moment so those columns are hidden most of the time.**
