# Spreadsheets

## Editing the spreadsheets

!!! warning "DO NOT EDIT THE DIRECTLY IN THE REPOSITORY!!!"

    Instead edit them on the google drive
    and then run type `tox run -e update` to update all the TSVs in the repository.

    The spreadsheets that allow us to generate the different checklists are hosted on this
    [google drive folder](https://drive.google.com/drive/folders/1wg5k-6pSB3mQm_a30abX6qb-lzTn_S-Y?usp=sharing)
    and we back them up as TSVs in the [main repo of the project](https://github.com/Remi-Gau/eCobidas).

    [:octicons-arrow-right-24: Back up the google sheets](./setup.md#update-the-tsvs)

## Available spreadsheets

### Apps

Some apps have their entire list of questions into a single spreadsheet.

{{ MACROS___table_apps() }}

### Reproschema "Activities"

Some sections of our checkists are kept in separate google sheets.

They are listed below.

{{ MACROS___table_spreadsheets() }}

### Preset responses

Some items have a long list of possible responses, or several items may share the same response set.

Those are kept in separate spreadhsheets and turned into [`ResponseOptions` JSON-LD](https://www.repronim.org/reproschema/schema/#responseoption).

{{ MACROS___table_preset_responses() }}

## Working with the spreadsheets

Here is a short list of the different things to keep in mind when working on one of the spreadsheet.

Each line must correspond to one checklist item that must have only one unambiguous item with an associated question.
Any item that opens the possibility of a response of the form:

```text
If A was used, then list the parameters B, C, D
```

Then it must be broken down into several questions:

```text
1. Was A used?
2. If so, what parameter was used for B?
3. What parameter was used for C?
...
```

For each item:

-   make sure it has a name, preferred label, description

-   make sure that there is a clear specific and unambiguous question associated to this item

-   identify the response type expected

-   create a response choice list where needed

-   mark the item as high-priority to be in the next release of the app.

-   assess whether there is way to **not** expose users to that item
    (or restrict list of the response choices for that item) if it is not relevant to their use-case

### Style guide

Where relevant we try to use `snake_case` and stick to lower case.

### Hidden columns

If some columns do not appear, it is possible that they have been hidden by
someone else. You will simply have to click on the double black arrow at the
limit between columns to display them back.

![](../img/show_hidden_columns.png)

### Filtering

If you want to only see certain rows, it is better to filter them rather than hide them.

The column headers can be used to filter which item to display:
for example, the `activity_name` column can be filtered using the arrow in the top cell in order
to see only the items corresponding to one or more main sections
(e.g., "Acquisition", "Experimental design", "Preprocessing", etc.).

## Spreadsheet content

The description of the columns common to all spreadsheet is described in the
[data dictionary](https://github.com/Remi-Gau/eCobidas/tree/main/ecobidas/inputs/data-dictionary.json).

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

{{ MACROS___table_data_dictionary() }}
