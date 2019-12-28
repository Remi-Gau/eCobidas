# COBIDAS checklist
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

-   [How to reach us](#How-to-reach-us)
-   [Why this project](#Why-this-project)
-   [Goals and roadmap](#Goals-and-roadmap)
-   [Implementation](#Implementation)
-   [How to contribute](#How-to-contribute)
-   [References](#References)


The prototype app for this checklist can be found here: https://cobidas-checklist.herokuapp.com/

This repository host the work turning the report published by the Committee on Best Practices in Data Analysis and Sharing (COBIDAS) of the organization for human brain mapping (OHBM) into a practical tool for improving methods and results reporting in neuroimaging and EEG/MEG.

This repository is a place where:
1. issues and ideas around reaching this goal are discussed;
2. plans for how to reach this goal are designed and implemented.


## How to reach us

If you want to be kept posted about the progress of the project, you can join our [google group](https://groups.google.com/d/forum/cobidas-checklist).

From more frequent updates and behind the scenes, come and join us on the `cobidas_checklist` channel on the brainhack mattermost. <a href="https://mattermost.brainhack.org/brainhack/channels/cobidas_checklist"><img src="http://www.mattermost.org/wp-content/uploads/2016/03/logoHorizontal.png" width=100px /> Join our channel </a>

Otherwise you can open a new issue on the repository itself if there is something you would like to discuss directly here.

There is also an [OSF project](https://osf.io/anvqy/) to centralize all the information and repos.

## Why this project

Poor methods and results description hinders the reproducibility and the replicability of research. It also makes it hard to compare new and old results and generally increases inefficiency in the research process. This project is built on the hope that improving methods and results reporting could improve our research.

See [here](./why_this_project.md) to for more background information.


## Goals and roadmap

**The short term goal of this project is to make the COBIDAS report easier to use: we want to create a website with a clickable checklist that automatically generates a method section at the end.**

By turning the checklist into a website users could more rapidly click through it and provide more of the information requested by the COBIDAS report. This would generate a small text file (a json file) that summarizes what option was chosen for each item of the checklist. This machine readable file could then be used to automatically generate part of the methods section of an article.

See [here](./goals.md) for more information on our short and long term goals as well as possible extension to the project. If you are interested by any of those get in touch. Many of them do not necessarily require super-advanced technical skills (except maybe a certain love for working with spreadsheet and wanting them to be super organized) :wink:.

We are still in development so we are currently using the [list of required inputs](./xlsx/metadata_neurovault.csv) from [neurovault](https://www.neurovault.org/) to work on the user interface.


## Implementation

The prototype app for this checklist can be found here: https://cobidas-checklist.herokuapp.com/

The first step of the implementation involves taking a spreadsheet that contains all the items of the checklist and turning that into a representation that can efficiently link the metadata about each item to the data imputed by the user. We are currently using the [schema-standardization](https://github.com/ReproNim/schema-standardization) initiative from [ReproNim](http://www.repronim.org/) to do this. Basically it means turning your 'dumb' spreadsheet into an equivalent but 'smarter' representation of it: a bunch hierarchically organized json files that link to each other.

On top of the inherent [advantages](https://github.com/ReproNim/schema-standardization#30-advantages-of-current-representation) of this schema representation:
-   its use simplifies the rendering of the checklist by using the [schema-ui](https://github.com/ReproNim/schema-ui) made for it,
-   this representation allows specification of user interface option that can simplify the user experience: it allows us to specify a branching logic that will prevent users to be presented with items that are not relevant to them (e.g answer PET related when they have only run an fMRI study).

See [here](./how_to_render_the_checklist.md) for more information.

## How to contribute

We are looking for people to give us feedback or help us move forward and implement all of this.

To learn more about the contributors and how to contribute see [here](./contributors.md).


## References

Jeanette Mumford has a [30 min video](https://www.youtube.com/watch?v=bsM4KowO5Vc&t=175s) explaining the background behind the COBIDAS report and giving a run through of the checklist.

The COBIDAS report:
- [for MRI and fMRI](https://www.biorxiv.org/content/10.1101/054262v2)
- [for EEG and MEG](https://osf.io/a8dhx/)
- MEEG report presentation at [OHBM 2019](https://www.pathlms.com/ohbm/courses/12238/sections/15843/video_presentations/138196)

The original [spreadsheet version](https://osf.io/qkb9t/) of the COBIDAS checklist (thanks to [Cass](https://github.com/cassgvp)!!!)

Presentation slides made about this project can be found in the [presentations folder](./presentations) and [here](./presentations/links.md).

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://remi-gau.github.io/"><img src="https://avatars3.githubusercontent.com/u/6961185?v=4" width="100px;" alt=""/><br /><sub><b>Remi Gau</b></sub></a><br /><a href="https://github.com/Remi-Gau/COBIDAS_chckls/commits?author=remi-gau" title="Code">💻</a> <a href="#design-remi-gau" title="Design">🎨</a> <a href="#content-remi-gau" title="Content">🖋</a> <a href="#ideas-remi-gau" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-remi-gau" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#maintenance-remi-gau" title="Maintenance">🚧</a> <a href="#projectManagement-remi-gau" title="Project Management">📆</a> <a href="#tool-remi-gau" title="Tools">🔧</a> <a href="#talk-remi-gau" title="Talks">📢</a></td>
    <td align="center"><a href="https://github.com/cassgvp"><img src="https://avatars2.githubusercontent.com/u/43407869?v=4" width="100px;" alt=""/><br /><sub><b>cassgvp</b></sub></a><br /><a href="https://github.com/Remi-Gau/COBIDAS_chckls/commits?author=cassgvp" title="Code">💻</a> <a href="#design-cassgvp" title="Design">🎨</a> <a href="#content-cassgvp" title="Content">🖋</a> <a href="#ideas-cassgvp" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-cassgvp" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#talk-cassgvp" title="Talks">📢</a></td>
    <td align="center"><a href="https://github.com/joyswe"><img src="https://avatars1.githubusercontent.com/u/47354027?v=4" width="100px;" alt=""/><br /><sub><b>joyswe</b></sub></a><br /><a href="https://github.com/Remi-Gau/COBIDAS_chckls/commits?author=joyswe" title="Code">💻</a> <a href="#design-joyswe" title="Design">🎨</a> <a href="#content-joyswe" title="Content">🖋</a> <a href="#ideas-joyswe" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-joyswe" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="https://github.com/fedeadolfi"><img src="https://avatars3.githubusercontent.com/u/26678283?v=4" width="100px;" alt=""/><br /><sub><b>Federico Adolfi</b></sub></a><br /><a href="https://github.com/Remi-Gau/COBIDAS_chckls/commits?author=fedeadolfi" title="Code">💻</a> <a href="#design-fedeadolfi" title="Design">🎨</a> <a href="#content-fedeadolfi" title="Content">🖋</a> <a href="#ideas-fedeadolfi" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-fedeadolfi" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="https://github.com/sanuann"><img src="https://avatars3.githubusercontent.com/u/5114945?v=4" width="100px;" alt=""/><br /><sub><b>Sanu Ann Abraham</b></sub></a><br /><a href="https://github.com/Remi-Gau/COBIDAS_chckls/commits?author=sanuann" title="Code">💻</a> <a href="#design-sanuann" title="Design">🎨</a> <a href="#infra-sanuann" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="http://www.nisox.org"><img src="https://avatars3.githubusercontent.com/u/5155907?v=4" width="100px;" alt=""/><br /><sub><b>Thomas Nichols</b></sub></a><br /><a href="#design-nicholst" title="Design">🎨</a> <a href="#content-nicholst" title="Content">🖋</a> <a href="#ideas-nicholst" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!