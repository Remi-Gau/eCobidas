# General organization

General workflow of this project:

1.  turning the recommendation guidelines into google sheets
1.  downloading the google sheets as TSVs
1.  turning the TSVs into a "schema" representation
1.  using a "front-end" user-interface that will read those schema and serve a web-app to the user.

To execute that work, this project is organized around several "repositories":

-   the [eCOBIDAS repository](https://github.com/Remi-Gau/eCobidas) centralises
    most of the information and workflow to convert the guidelines into a
    checklist webapp,

-   the [Reproschema user interface](https://github.com/ReproNim/reproschema-ui)
    contains the "front-end" code of the user interface to render the checklist
    webapp,

-   the [ReproSchema](https://github.com/ReproNim/reproschema) repository
    contains the formal "definition" of the terms used to describe the content
    of the checklist as a schema,

-   the repositories containing a) an instance of the user interface and b) a
    schema to serve a specific checklist :

    -   the [one for the MRI version](https://github.com/ohbm/cobidas) based of
        the Neurovault metadata "checklist" hosted on the OHBM Github
        organization and that serves this
        [checklist](https://ohbm.github.io/eCOBIDAS/#/),

    -   the one for the
        [PET imaging version](https://github.com/Remi-Gau/cobidas-PET) that
        serves this [checklist](https://remi-gau.github.io/cobidas-PET/#/),

-   the
    [google drive](https://drive.google.com/drive/folders/1wg5k-6pSB3mQm_a30abX6qb-lzTn_S-Y?usp=sharing)
    where we work synchronously on the
    [spreadsheets](https://drive.google.com/drive/folders/1ydwALHDzl21dcef3qhkju8JKKAT3Y72V?usp=sharing),

-   an associated
    [zotero library](https://www.zotero.org/groups/2349772/cobidas_checklist) to
    keep track of references related to this project,

-   a [project on the open-science framework](https://osf.io/anvqy/) that allows
    to "connect" all those elements together in one place.

## the eCOBIDAS repository

This repository hosts the workflow that will turn the reports published by the
Committee on Best Practices in Data Analysis and Sharing (COBIDAS) of the
organization for human brain mapping (OHBM) into a checklists for improving
methods and results reporting in (f)MRI, (i)EEG, MEG.

By extension, this workflow can also be used on other types of guidelines (like
the ones for PET imaging and eyetracking).

```bash
📂
┣━━ 📂 docs
┣━━ 📂 ecobidas
┃   ┣━━ 📂 inputs
┃   ┃   ┣━━ 📂 core
┃   ┃   ┣━━ 📂 eyetracking
┃   ┃   ┣━━ 📂 meeg
┃   ┃   ┣━━ 📂 mri
┃   ┃   ┣━━ 📂 neurovault
┃   ┃   ┣━━ 📂 pet
┃   ┃   ┣━━ 📂 reexecution
┃   ┃   ┣━━ 📂 response_options
┃   ┃   ┣━━ 📄 data-dictionary.json
┃   ┃   ┗━━ 📄 spreadsheet_google_id.yml
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
┣━━ 📂 schema # (1)
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

1.  :man_raising_hand: I'm an annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be expressed in Markdown.




```text
.
├── .github           <-- continuous integration "scripts"
├── activities        <-- deprecated: ignore this
├── communication     <-- abstracts and presentations about the project
├── docs              <-- content of the documentation
├── inputs            <-- checklists spreadsheets as CSV files, boilerplate for method section generation
├── schema            <-- deprecated: ignore this
├── schemas           <-- where the schemas are kept locally
├── python            <-- python package to convert the CSV spreadsheets into schemas
└── tests             <-- python script to test that the schema files are valid JSON-LD
```

In the schemas folder you might find different folders some of them with the
following names:

```text
├── protocols         <-- schema for the checklists putting together several "sections" together
├── activities        <-- schema of the different "sections"of the checklistss with their items
└── response_options  <-- contains the pre-set list of response options to some checklist items
```

### Spreadsheet content and organization

The first step of the workflow involves taking the recommendation guidelines and
converting that into a spreadsheet that contains all the items of the future
checklist.

This step is by far the most labor intensive and has its dedicated page in the
[documentation](./spreadsheets.md)

### Converting the spreadsheet into a schema

Most of that is covered in the section on
[how the checklist is rendered](./how-to-render-the-checklist.md) and in the
README in the `python` folder.

## How is the Reproschema organized

The first step of the workflow involves taking a spreadsheet that contains all
the items of the checklist and turning that into a representation that can
efficiently link the metadata about each item to the data imputed by the user.
We are using the [ReproSchema](https://github.com/ReproNim/reproschema)
initiative from [ReproNim](http://www.repronim.org/) to do this. Basically, it
means turning your 'dumb' spreadsheet into an equivalent but 'smarter'
representation of it: a bunch of hierarchically organized json files that link
to each other.

On top of the inherent
[advantages](https://github.com/ReproNim/reproschema#30-advantages-of-current-representation)
of this schema representation:

-   its use simplifies the rendering of the checklist by using the
    [reproschema-ui](https://github.com/ReproNim/reproschema-ui) made for it,

-   this representation allows specification of user interface option that can
    simplify the user experience: it allows us to specify the conditions that
    will make certain items visible or not and thus will prevent users to be
    presented with items that are not relevant to them (e.g answer PET related
    when they have only run an fMRI study).

The reproschema is organized in a hierarchical manner with several levels, the
main ones being

1.  The lowest level is the `item level` where there is one question for each
    item with an expected format for the user interface: is this yes / no
    question (boolean), a multiple choice, a float or an integer...

1.  The second level is the `activity level` that contains a set of items. In
    the original repronim project this would constitute usually a questionnaire:
    like all the items of the Edinburgh handedness inventory would constitute
    one activity. In our case, we are using it to define to break a checklist
    into sub-sections of a method section like preprocessing, design,
    participants...

1.  The highest level is the `protocol level` that contains a set of activities.
    At the moment this level is under-used in our checklist but could be used to
    define activity sets for different use case: fMRI, MEEG, pre-registration...

If you want to know more about Reproschema, we suggest you have look at the
documentation

-   [main documentation](https://www.repronim.org/reproschema/)
-   [FAQ](https://www.repronim.org/reproschema/FAQ/)
