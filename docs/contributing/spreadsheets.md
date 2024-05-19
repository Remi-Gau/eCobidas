# Spreadsheets

The spreadsheets that allow us to generate the different checklists are hosted
on this
[google drive folder](https://drive.google.com/drive/folders/1wg5k-6pSB3mQm_a30abX6qb-lzTn_S-Y?usp=sharing)
and we try to keep a back-up in the
[folder](https://github.com/Remi-Gau/eCobidas/tree/main/ecobidas/inputs).

The
?? will directly download those spreadsheets as csv files into the
`inputs` folder.

<!-- generate the table below using python/app_list_table.py -->

| web app                                                                                                                                                                         | reference                                                             | spreadsheet                                                                                                                       | Github repository                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [COBIDAS MRI](https://ohbm.github.io/eCOBIDAS/#/)                                                                                                                               | [link](http://www.humanbrainmapping.org/files/2016/COBIDASreport.pdf) |                                                                                                                                   |                                                          |
| [neurovault](https://www.repronim.org/reproschema-ui/#/?url=https://raw.githubusercontent.com/ohbm/cobidas_schema/master/schemas/neurovault/protocols/neurovault_schema.jsonld) | [link](https://doi.org/10.3389/fninf.2015.00008)                      | [spreadsheet](https://docs.google.com/spreadsheets/d/1arizMF2GnaiXz9txY5tzTU7uoA0_ENE17W5wDeUPpu0/edit?usp=sharing)               |                                                          |
| [pet](https://remi-gau.github.io/cobidas-PET/#/)                                                                                                                                | [link](https://doi.org/10.1177/0271678X20905433)                      | [spreadsheet](https://docs.google.com/spreadsheets/d/1HS-1KOP8nE7C3MHiyRmQ6hd823cBZnCRVq0UryXvDc8/edit?usp=sharing)               | [github](https://github.com/Remi-Gau/cobidas-PET)        |
| [eyetracking](https://remi-gau.github.io/cobidas-eyetracker/#/)                                                                                                                 | [link](https://psyarxiv.com/f6qcy/)                                   | [spreadsheet](https://docs.google.com/spreadsheets/d/1aQZINzS24oYDgu6PZ8djqZQZ2s2eNs2xP6kyzHokU8o/edit?usp=sharing)               | [github](https://github.com/Remi-Gau/cobidas-eyetracker) |
| [artemis](https://remi-gau.github.io/artemis_checklist/#/)                                                                                                                      | [link](https://osf.io/pvrn6/)                                         | [spreadsheet](https://docs.google.com/spreadsheets/d/1dlUt8_bHsM5mERFJkVLTVWanSlms6Ba8Wos38Dhmhfo/edit?ts=60c9d280#gid=759849853) | [github](https://github.com/Remi-Gau/artemis_checklist)  |
| [reexecution](https://remi-gau.github.io/cobidas_reexecute/#/)                                                                                                                  | [link](https://doi.org/10.12688/f1000research.25306.2)                | [spreadsheet](https://docs.google.com/spreadsheets/d/1M9H7Bkti4OEVrYETajLbpbwY0T-QqSkpRUiwTz6-5Vc/edit?usp=sharing)               | [github](https://github.com/Remi-Gau/cobidas_reexecute)  |

## To do

Here is a short list of the different things to keep in mind when working on one
of the spreadsheet.

Each line must correspond to one checklist item that must have only one
unambiguous item with an associated question. Any item that opens the
possibility of a response of the form:

```bash
If A was used, then list the parameters B, C, D
```

Then it must be broken down into several questions:

```bash
1. Was A used?
2. If so, what parameter was used for B?
3. What parameter was used for C?
...
```

For each item:

-   make sure it has a name, preferred label, description: for some of those a
    formula in the spreadsheet should automatically take care of that

-   make sure that there is a clear specific and unambiguous question associated
    to this item

-   identify the response type expected

-   create a response choice list where needed

-   mark the item as high-priority to be in the next release of the app.

-   assess whether there is way to **not** expose users to that item (or
    restrict list of the response choices for that item) if it is not relevant
    to their use-case

<!-- TODO add examples -->

## Working with the spreadsheets

This describes some rules and tips when working with the spreadsheets.

### Style guide

Where relevant we try to use `snake_case` and stick to lower case.

### Hidden columns

If some columns do not appear, it is possible that they have been hidden by
someone else. You will simply have to click on the double black arrow at the
limit between columns to display them back.

![](../img/show_hidden_columns.png)

### Formatting

The MRI spreadsheet has some conditional formatting implemented so some cells
will appear red when there is an error to be fixed (or if the cell is empty and
should be filled). Some items that require more work might be manually
highlighted in orange.

### Filtering

If you want to only see certain rows, it is better to filter them rather than
hide them.

The column headers can be used to filter which item to display: for example, the
`activity_name` column can be filtered using the arrow in the top cell in order
to see only the items corresponding to one or more main sections (e.g.,
"Acquisition", "Experimental design", "Preprocessing", etc.).

## Formulas and automation

There is a certain level of automation built into those spreadsheets to fill in
certain columns. For example, the preferred label of an item is generated from
the item name by removing any underscore.

Given that some of the guidelines used as source material often had several sub
and sub-sub-sections organized in a hierarchical fashion, this was in some cases
used to generate the item names.

Below is an example how the item name for the MRI spreadsheet is determined by
the content of the right-most non-empty column on the lef of the item column.

|                              |                  |                 | item_name       |
| ---------------------------- | ---------------- | --------------- | --------------- |
| Imaging type                 |                  |                 | imaging_type    |
| Essential imaging parameters | All acquisitions | voxel dimension | voxel_dimension |
| Essential imaging parameters | Slice timing     |                 | slice_timing    |

## Spreadsheet content

Here follows a description of the columns' content.

### Content common to all spreadsheets

The description of the columns common to all spreadsheet is described in the
[data dictionary](https://github.com/Remi-Gau/eCobidas/tree/main/ecobidas/inputs/data-dictionary.json)
in the
[inputs folder](https://github.com/Remi-Gau/eCobidas/tree/main/inputs/).

Each column is described by an element in the JSON data dictionarry.

```JSON
"column_name": {
    "LongName": "",
    "VariableName": "name of the corresponding variable, if relevant, in the conversion scripts",
    "Description": "",
    "Levels": "describes the different possibilities in this column"
}
```

<!-- TODO automatically generate this section with data dictionaries of the spreadsheets -->

## preset responses

<!-- generate the table below using python/app_list_table.py -->

| response list                   | google spreadsheet                                                                                                  | jsonld                                                                                                               |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| mri_softwares                   | [spreadsheet](https://docs.google.com/spreadsheets/d/1TT38bvZimEnfBdp4O0i2_YEnUk9J60QXAJykGSxJsjI/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/mri_softwares.jsonld)                   |
| stimulus_presentation_softwares | [spreadsheet](https://docs.google.com/spreadsheets/d/1Gal7vMIJk4EOa1XrKgioLyfAvQJKQQDSw3YlEAeCecA/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/stimulus_presentation_softwares.jsonld) |
| multiple_comparisons            | [spreadsheet](https://docs.google.com/spreadsheets/d/19-030DcknqEL-aSYhG-BwosMGQo_WMvyiveita5wLv8/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/multiple_comparisons.jsonld)            |
| interpolations                  | [spreadsheet](https://docs.google.com/spreadsheets/d/1aN4HzzZLcc_IywvuXqOzlqApl7v2NBGcHSjUTmEWlEo/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/interpolations.jsonld)                  |
| cost_functions                  | [spreadsheet](https://docs.google.com/spreadsheets/d/1MWyPZ_EpaJ8qxQJOH5Zmnibl0npcewHtDIH5Yfgtx-c/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/cost_functions.jsonld)                  |
| meeg_reference_electrodes       | [spreadsheet](https://docs.google.com/spreadsheets/d/11GXVYHfqMOCnU7jeBR0MZQbUU1rUh2Jf8DSRAEAPsV0/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/meeg_reference_electrodes.jsonld)       |
| meeg_analysis_softwares         | [spreadsheet](https://docs.google.com/spreadsheets/d/1HIZddFerYChctkUANE7AAoQXVA8B_1rKnjXpw3XkS6Q/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/meeg_analysis_softwares.jsonld)         |
| meeg_amplifier_brands           | [spreadsheet](https://docs.google.com/spreadsheets/d/1fIw2DLSCBpNQ0WnGmbbV1G7L5bywXkNCTNP_UFroNe0/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/meeg_amplifier_brands.jsonld)           |
| meeg_acquisition_softwares      | [spreadsheet](https://docs.google.com/spreadsheets/d/10qiox_kb-F0RjF1vfd1B8dyZMF7kF9UoMBHrfW-IqLA/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/meeg_acquisition_softwares.jsonld)      |
| eeg_cap_types                   | [spreadsheet](https://docs.google.com/spreadsheets/d/1Wy6Vts1ruSFqLZ4Ftfuq2vP4rASfZBe1RCzjHECVRL0/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/eeg_cap_types.jsonld)                   |
| boolean                         | [spreadsheet](https://docs.google.com/spreadsheets/d/1l8_89p6zCrku7ETqThXZvpy6BvIwnFhPfNRIXn1bmcU/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/boolean.jsonld)                         |
| spm_version                     | [spreadsheet](https://docs.google.com/spreadsheets/d/1ZfxJdQ-a9Y-hoY37jZN8stPHjQmyHxQKM3wEhv8MqAo/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/spm_version.jsonld)                     |
| linux_version                   | [spreadsheet](https://docs.google.com/spreadsheets/d/1UQhId75_vEBfsJOtoZK2caeiJCCWuxWwJtUxcdNa8pg/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/linux_version.jsonld)                   |
| type_os                         | [spreadsheet](https://docs.google.com/spreadsheets/d/1tPBQArrw_vXPvR2JKURmCrW4Ldbi2Yta83QAyyqHdfs/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/operating_systems.jsonld)               |
| windows_version                 | [spreadsheet](https://docs.google.com/spreadsheets/d/1wGN4pP4tojxxqH3baEa6DbDaGjRgjebu-SuLYMhRzmw/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/windows_version.jsonld)                 |
| macos_version                   | [spreadsheet](https://docs.google.com/spreadsheets/d/1fLyrEbnxj4Y-XWOfvTcaJuZNxDOHGh_nEJ1vXJdJS9E/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/macos_version.jsonld)                   |
| eyetracker_preproc_softwares    | [spreadsheet](https://docs.google.com/spreadsheets/d/1MrDCAoQvDbKr59LT1_lJB8SnXMhxJnRDATLXciA4Jys/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/eyetracker_preproc_softwares.jsonld)    |
| eyetracker_model_name           | [spreadsheet](https://docs.google.com/spreadsheets/d/14Zo4ltjKOyiJ9wUd5ZybMt6MnEryMc23KAb7sspT0Ko/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/eyetracker_model_name.jsonld)           |
| eyetracker_producer             | [spreadsheet](https://docs.google.com/spreadsheets/d/1SxM0c3QgRprfPM8KL8SBRaUGCGKzRKFG4apZ2NwcpqM/edit?usp=sharing) | [jsonld](https://github.com/ohbm/cobidas_schema/blob/master/response_options/eyetracker_producer.jsonld)             |

## Extra columns

-   Software defaults columns (`spm_default`, `fsl_default`) refer to the
    default value used for this item by a given software.

-   Integration with other sources:

    -   Brain Imaging Data Structure dataset: the `bids_*` columns denote if
        information about this item can be found in a
        [BIDS](http://bids.neuroimaging.io/) dataset and if so where.

    -   `nidm_results`: mention where information this item can be found in an
        NIDM results package

    -   `neurovault` collection: refers to the name of this item in a Neurovault
        collection

-   Meta-analysis: These columns denote whether or not each item could be
    important to evaluate studies for a meta-analysis.

    -   `use_case_meta-analysis`

        -   yes, include for meta-analyses
        -   no, exclude for meta-analyses
        -   maybe - `meta-analysis_comment`

### Percent of studies reporting the item

Comparison to Carp 2012

Some columns list the percentage of studies that reported each item.

For the MRI spreadsheet, this is taken from
[Carp, 2012](https://drive.google.com/file/d/1TBSxC52kXVERl9JmfbBPC7uCas4QN_vg/view?usp=sharing).

-   `in_Carp2012`: name of the item in that paper

-   `percent_of_studies`: percent of studies reporting the item. If the number
    is in **bold**, it was approximately extracted from one of the figures of
    the paper. (because it was not reported in the text of the article).

-   `percent_of_studies_anat`: same as above but for the anatomical data

The Eyetracking spreadsheet `percent_reported` column also has numbers on the
frequency at which items are present in the literature (see the
[preprint](https://psyarxiv.com/f6qcy/))
