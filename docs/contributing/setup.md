
# Setup

## Requirements

You will need to have installed.

-   Python
-   [node.js](https://nodejs.org/en/)
-   [Git](https://git-scm.com/downloads)

## Install

Fork and clone the repository with all its submodules.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/eCobidas.git --recurse-submodules
```

The easiest way to install all the Python dependencies for this project is then to run:

```bash
pip install -r requirements.txt
```

## Visual studio code settings

Load the `ecobidas.code-workspace` file in the `.vscode` folder.

## Tox

Several maintenance tasks are automated with tox.

To install tox (in case in it was not installed by the command above):

```bash
pip install tox
```

To known the available "recipes" that tox can run:

```bash
tox list
```

To run a recipe

```bash
tox run -e <recipe_name>
```

For example `tox run -e convert` will convert all the TSVs containing all the checklists into JSONLD files.

## Command line interface

The python tooling in the `ecobidas` folder for this project is packaged as a python package with a CLI.

To know more about what it can do.

```bash
ecobidas --help
```

## Update the TSVs

All the spreadsheets of the project can be downloaded from the google drive with tox:

```bash
tox run -e update
```

This relies on the CLI:

```bash
ecobidas update
```

## Generate the schemas

Tox can be used to convert all the TSVs of the project to their reproschema JSON-LD equivalent:

```bash
tox run -e convert
```

This relies on the CLI:

```bash
ecobidas convert
```

### Validate the JSON-LD

All the JSON-LD generated can be validated with tox

```bash
tox run -e validate_all
```

This uses the `reproschema` python package from the `reproschema-py` submodule.

This also relied on `make` to run the validation recipes
from the `artemis_schema` and `cobidas_schema` git submodules.

If you do not have make installed, do not worry the github continuous integration can run those validations for you.

## Style guide

All our formatting and linting is implemented through tox and pre-commit.

To apply them, install tox and then just type the following in your terminal.

```bash
tox
```

### Markdown

-   For markdown styling we rely on [remark](https://github.com/remarkjs/remark-lint).
-   We check for dead links using the [markdown-link-check](https://github.com/marketplace/actions/markdown-link-check) github action.
