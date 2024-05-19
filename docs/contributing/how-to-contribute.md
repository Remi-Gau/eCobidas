# How to contribute

---

**Join our working group at the
[International Neuroinformatics Coordinating Facility](https://www.incf.org/sig/incfohbm-working-group-checklists-transparent-methods-reporting-neuroscience-ecobidas)**

---

There are many ways in which you can contribute to this project.

We have a list of [milestones](../goals/goals.md)
for the different features we would like to include in this project.

Those milestones have
[several opened issues](https://github.com/Remi-Gau/eCobidas/issues) related to them:
have a look through those issues to see if there is any of them where you think you can help.

We are also track the progress to our different goals
using some of the integrated [kanban boards](https://github.com/Remi-Gau/eCobidas/projects) that github offers.

## Suggestions

If you are unsure where to start, maybe have a read through some of those
sections about the project. It might give you ideas.

-   the [motivations](../motivations.md) of this project
-   the [different short and long term goals](../goals//goals.md)
-   the [general organization of the project](./general-organization.md)

Otherwise here are some suggestions of the different tasks that you can contribute to.
If however you feel more interested to start hacking at some of the issues related to long other goals, feel free to do so.

### Spreadsheets

A lot of the work requires to interact with the checklists in their spreadsheet
format.

The spreadsheets are hosted on this
[google drive folder](https://drive.google.com/drive/folders/1wg5k-6pSB3mQm_a30abX6qb-lzTn_S-Y?usp=sharing)
and we try to keep a back-up in the
[csv folder](https://github.com/Remi-Gau/eCobidas/tree/main/inputs).

The MRI part is the more advanced at this moment but we are looking for people
to help with the M/EEG part.

The content of the spreadsheets and the work involved there is described in more
details [here](./spreadsheets.md).

### Boilerplate method sections

We want to create
[boilerplate method sections](https://github.com/Remi-Gau/eCobidas/tree/main/inputs/boilerplate)
corresponding to a single item or a set of items of the checklist to automate
methods writing once the checklist is completed. There is a lot of work to do
there in terms of writing the boilerplate text as well as automating the methods
section generation.

Boilerplate related issues listed
[here](https://github.com/Remi-Gau/eCobidas/issues?q=is%3Aissue+is%3Aopen+label%3Aboilerplate).

### Documentation

If you don't understand something about the project, its goals, its
implementation or how to use, then it's most likely that we did not do a good
enough job at explaining and describing it.
[Get in touch](../contact.md)
and we can work together to improve our documentation.

There are also
[several aspects of the documentation](https://github.com/Remi-Gau/eCobidas/issues?q=is%3Aissue+is%3Aopen+label%3Adocumentation)
that need to be expanded.

### Conversion scripts

We use some
[python code](https://github.com/Remi-Gau/eCobidas/tree/main/ecobidas) to
convert the spreadsheets into the set of `jsonld` files that the user interface
needs as inputs to display the checklists. This needs further improvement so if
python is your jam, feel free to dive in.

We are also using the
[Reproschema python package](https://github.com/ReproNim/reproschema-py) to
validate the schemas created. This package should also in the long-term help
automating the creation of schemas, so there are definitely some features
waiting to be written there.

There is more information on how to set things up in the
[CONTRIBUTING.md](./CONTRIBUTING.md).

### User interface

The [user interface](https://github.com/ReproNim/schema-ui) is Javascript based
and uses the [Vue framework](https://vuejs.org/) and this also needs a lot of
tweaking, so if Javascript is cup of tea:
[get in touch!](../contact.md)

Here are
[some of the issues](https://github.com/Remi-Gau/eCobidas/issues?q=is%3Aissue+is%3Aopen+label%3Auser-interface)
related to the UI.

## Style guide

### Python

We rely on [black](https://github.com/psf/black) to automate the python code
formatting.

We have additional checks on Github for code style and quality.

-   [pep8 speaks](https://github.com/marketplace/pep-8-speaks) for code style

-   the awesome [sourcery](https://github.com/marketplace/sourcery-ai) for code
    quality and refactoring suggestions.

### Markdown

-   For markdown styling we rely on
    [remark](https://github.com/remarkjs/remark-lint).

-   We check for dead links using the
    [markdown-link-check](https://github.com/marketplace/actions/markdown-link-check)
    github action.
