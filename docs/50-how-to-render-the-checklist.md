# How the checklist is rendered

<!-- TOC -->

-   [How the checklist is rendered](#how-the-checklist-is-rendered)
    -   [How to](#how-to)
        -   [Turn the spreadsheet into the schema](#turn-the-spreadsheet-into-the-schema)
        -   [Making the new schema available to the cobidas-ui](#making-the-new-schema-available-to-the-cobidas-ui)
        -   [Rendering the checklist](#rendering-the-checklist)
            -   [Run Locally with node.js](#run-locally-with-nodejs)

<!-- /TOC -->

First make sure you understand how the different part of this project are
organized by reading the [general organization](./general_organization.md)
document.

---

## How to

### Turn the spreadsheet into the schema

<!-- TODO add link to script section -->


### Making the new schema available to the cobidas-ui

If the previous step went smoothly you now need to make the newly created files
available on the remote of your reproschema repository so that the cobidas-ui
repository can 'see' them. This you can do by committing the files newly created
on your local reproschema repository and pushing them the remote. For example if
the schema is hosted on the `neurovault` branch of your `origin` remote
repository, the following should do the trick (assuming that you are already on
the `neurovault` branch of your local repo):

```
git add --all
git commit -m 'update neurovault schema'
git push origin neurovault
```

### Rendering the checklist

<!-- TODO add link to doc of the ui -->

Step inside the `cobidas-ui` directory, checkout the `neurovault` development
branch

```
cd cobidas-ui
git checkout neurovault
```

Make sure that that you have set `cobidas-ui` correctly so it will read the
schema from the right repository. This can be be set by modifying its
`schema-ui/src/config.js` file (e.g see
[here](https://github.com/Remi-Gau/cobidas-ui/blob/COBIDAS/src/config.js)).

You then have 2 options to run the app locally: use javascript `node.js` or use
`docker`.

#### Run Locally with node.js

-   Install [node version manager](https://github.com/nvm-sh/nvm) to help you
    deal with different version of `node.js`.

If you are running linux go for:

```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
```

Then close your terminal and reopen it then run

```
nvm install node
nvm install 9
```

-   Install the javascript dependencies
-   Run the development server

```
npm install
npm run dev
```

-   Open your browser and go to [localhost:8080](localhost:8080)
