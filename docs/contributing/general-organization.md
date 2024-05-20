# General organization

General workflow of this project:

``` mermaid
graph TD
  A[Google Sheet] --> |tox run -e update| B[📂 ecobidas/inputs/*/*.tsv];
  B -->|tox run -e convert| C[📂 cobidas_schema/schemas/**/*.jsonld];
  C -->|npm run serve| D[web app];
```

1.  turning the recommendation guidelines into google sheets
1.  downloading the google sheets as TSVs
1.  turning the TSVs into a "Reproschema" representation as JSON-LD
1.  using a "front-end" user-interface that will read those schema and serve a web-app to the user.

To execute that work, this project is organized around several "repositories".

A [project on the open-science framework](https://osf.io/anvqy/) allows
to "connect" all those elements together in one place.

Our [google drive](https://drive.google.com/drive/folders/1wg5k-6pSB3mQm_a30abX6qb-lzTn_S-Y?usp=sharing)
where we work synchronously on the [spreadsheets](https://drive.google.com/drive/folders/1ydwALHDzl21dcef3qhkju8JKKAT3Y72V?usp=sharing).

## the eCOBIDAS repository

This repository hosts:
-   the workflow that will turn reporting guidelines into a web-based checklists
-   the checklist saved as TSVs
-   the documentation for the project

See the tree below for more details.

```bash
📂
┣━━ 📂 .github
┣━━ 📂 docs
┣━━ 📂 artemis_schema # (8)
┣━━ 📂 cobidas_schema # (9)
┣━━ 📂 ecobidas # (1)
┃   ┣━━ 📂 inputs # (2)
┃   ┃   ┣━━ 📂 core
┃   ┃   ┣━━ 📂 eyetracking
┃   ┃   ┣━━ 📂 meeg
┃   ┃   ┣━━ 📂 mri
┃   ┃   ┣━━ 📂 neurovault
┃   ┃   ┣━━ 📂 pet
┃   ┃   ┣━━ 📂 reexecution
┃   ┃   ┣━━ 📂 response_options
┃   ┃   ┣━━ 📄 data-dictionary.json # (3)
┃   ┃   ┗━━ 📄 spreadsheet_google_id.yml # (4)
┃   ┣━━ 📂 templates
┃   ┣━━ 🐍 __init__.py
┃   ┣━━ 🐍 cli.py
┃   ┣━━ 🐍 create_schema.py
┃   ┣━━ 🐍 download_tsv.py
┃   ┣━━ 🐍 generate_landing_page.py
┃   ┣━━ 🐍 item.py
┃   ┣━━ 🐍 macros.py
┃   ┣━━ 🐍 parsers.py
┃   ┣━━ 🐍 serve.py
┃   ┣━━ 🐍 template_manager.py
┃   ┗━━ 🐍 utils.py
┣━━ 📂 inputs
┃   ┣━━ 📂 bids_template
┃   ┗━━ 📂 boilerplate
┣━━ 📂 macros
┣━━ 📂 reproschema-py # (5)
┣━━ 📂 reproschema-ui # (6)
┣━━ 📂 schema # (7)
┣━━ 📂 tests
┣━━ 📄 CITATION.cff
┣━━ 📄 LICENSE
┣━━ 📄 Makefile
┣━━ 📄 mkdocs.yml
┣━━ 📄 pyproject.toml
┣━━ 📄 README.md
┣━━ 📄 requirements.txt
┗━━ 📄 tox.ini
```

<!-- ANNOTATIONS START -->

1.  [python package](./setup.md#command-line-interface) to convert the TSV spreadsheets into schemas

2.  checklists spreadsheets as TSV files

3.  [data dictionary](./spreadsheets.md#spreadsheet-content) describing the content of the spreadsheets

4.  configuration file describing the information for each spreadsheet (sourcce, name, ...)

6.  [Reproschema python package](https://github.com/ReproNim/reproschema-py) to help convert TSVs into JSON-LD

6.  [Reproschema user interface](https://github.com/ReproNim/reproschema-ui)
    contains the "front-end" code of the user interface to render the checklist webapp

7.  deprecated: ignore this

8.  [cobidas_schema](https://github.com/ohbm/cobidas_schema.git) submodule where the JSON-LD files are stored.

9.  [artemis_schema](https://github.com/INCF/artem-is.git) submodule where the TSVs and JSON-LD files of the ARTEM-IS project are stored.

<!-- ANNOTATIONS END -->

### Apps repository

Checklist apps are deployed from their own repository
that are made to clone an instance of the [Reproschema user interface](https://github.com/ReproNim/reproschema-ui)
and pointing to a Reproshema protocol it's supposed to render.

Each repo is listed under the `GitHub repository` column of this table.

{{ MACROS___table_apps() }}

## How is the Reproschema organized

In the `cobidas_schema` repository you find different folders some of them with the following names:

```bash
cobidas_schema
┣━━ 📂 response_options # (1)
┗━━ 📂 schemas
    ┣━━ 📂 activities # (2)
    ┗━━ 📂 protocols # (3)
```

<!-- ANNOTATIONS START -->
1.  contains the [preset list of response options](./spreadsheets.md#preset-responses) to some checklist items
2.  schema of the different "sections"of the checklistss with their items
3.  schema for the checklists putting together several "sections" together
<!-- ANNOTATIONS END -->

The first steps of the workflow involves taking a spreadsheet that contains all the items of the checklist
and turning that into a representation that can efficiently link the metadata about each item
to the data imputed by the user.
We are using the [ReproSchema](https://github.com/ReproNim/reproschema) initiative
from [ReproNim](http://www.repronim.org/) to do this.
Basically, it means turning your 'dumb' spreadsheet into an equivalent
but 'smarter' representation of it:
a bunch of hierarchically organized json files that link to each other.

The reproschema is organized in a hierarchical manner with several levels,
the main ones being

1.  The lowest level is the `item level` where there is one question for each item
    with an expected format for the user interface:
    is this yes / no question (boolean), a multiple choice, a float or an integer...

1.  The second level is the `activity level` that contains a set of items.
    In the original repronim project this would constitute usually a questionnaire:
    like all the items of the Edinburgh handedness inventory would constitute one activity.
    In our case, we are using it to define to break a checklist into sub-sections of a method section
    like preprocessing, design, participants...

1.  The highest level is the `protocol level` that contains a set of activities.
    At the moment this level is under-used in our checklist
    but could be used to define activity sets for different use case:
    fMRI, MEEG, pre-registration...

The [ReproSchema](https://github.com/ReproNim/reproschema) repository
contains the formal "definition" of the terms used to describe the content of the checklist as a schema,

If you want to know more about Reproschema, have look at its documentation

-   [main documentation](https://www.repronim.org/reproschema/)
-   [FAQ](https://www.repronim.org/reproschema/FAQ/)
