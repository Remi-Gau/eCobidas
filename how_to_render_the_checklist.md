# How the checklist is rendered

The prototype app for this checklist can be found here: https://cobidas-checklist.herokuapp.com/

The first step of the implementation involves taking a spreadsheet that contains all the items of the checklist and turning that into a representation that can efficiently link the metadata about each item to the data imputed by the user. Basically it means turning your 'dumb' spreadsheet into an equivalent but 'smarter' representation of it: in this case a bunch hierarchically organized json files that link to each other.

So far most of the work is being done on spreadsheets hosted on this [google drive folder](https://drive.google.com/drive/folders/1wg5k-6pSB3mQm_a30abX6qb-lzTn_S-Y?usp=sharing) but you also find recent updates in the [xlsx folder](./xlsx/me).

In terms of choice of representation we are currently using the [schema-standardization](https://github.com/ReproNim/schema-standardization) initiative from [ReproNim](http://www.repronim.org/) to do this. On top of the inherent [advantages](https://github.com/ReproNim/schema-standardization#30-advantages-of-current-representation) of this schema representation:
-   its use simplifies the rendering of the checklist by using the [schema-ui](https://github.com/ReproNim/schema-ui) made for it,
-   this representation allows specification of user interface option that can simplify the user experience: it allows us to specify a branching logic that will prevent users to be presented with items that are not relevant to them (e.g answer PET related when they have only run an fMRI study).

So far we have a [script](./python/create_neurovault_schema.py) to turn the neurovault [list of required inputs](./xlsx/metadata_neurovault.csv) into a schema that can then be render with the schema-ui.

What follows is a quick "how to" if you want to render the checklist.

## General organization

There are 3 repositories needed to "render" this checklist:

-   this [COBIDAS_chckls repository](https://github.com/Remi-Gau/COBIDAS_chckls/) where you are currently reading this. It contains:
-   the [neurovault spreadsheet](./xlsx/metadata_neurovault.csv)
-   the python [script](./python/create_neurovault_schema.py) to turn that spreadsheet into a Repronim schema (basically a bunch hierarchically organized json files that link to each other).
-   this [fork of the ReproNim schema-standardization repository](https://github.com/Remi-Gau/schema-standardization) that hosts the schema representation of the checklist
-   the [cobidas-ui repository](https://github.com/Remi-Gau/cobidas-ui) that does the actual rendering the checklist app by reading the schema hosted by the previous repository. There is a general explanation of how the app works in this [issue](https://github.com/ReproNim/schema-ui/issues/4).

You will need to fork and clone each of them if you want to work on the checklist on your own. If you want some stable versions of the repositories this table gives you link to the most recent ones.

| Repositories                                                                            | Used version                                                                     |
|-----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| [COBIDAS checklist repository](https://github.com/Remi-Gau/COBIDAS_chckls/)             | [v0.0.1](https://github.com/Remi-Gau/COBIDAS_chckls/releases/tag/v0.0.1)         |
| [schema-standardization repository](https://github.com/Remi-Gau/schema-standardization) | [v0.0.1](https://github.com/Remi-Gau/schema-standardization/releases/tag/v0.0.1) |
| [cobidas-ui repository](https://github.com/Remi-Gau/cobidas-ui)                         | [v0.0.1](https://github.com/Remi-Gau/cobidas-ui/releases/tag/v0.0.1)             |

___

**WARNING**

If you are trying to render the checklist and it does not work, it could mean that some of the schema references could point to URI whose content might have changed. The best in this case is to git rebase the most recent changes on the master branch on the ReproNim schema-standardization repository onto the branch you are trying to render.
____

## How to

### Turn the spreadsheet into the schema

This can be done by running the `create_neurovault_schema.py` [python script](./python/create_neurovault_schema.py) but first make sure you modify the lines in the header so that the script matches your need:
-   you will need to change the URL of the repository where the schema will be hosted (currently set to `https://raw.githubusercontent.com/Remi-Gau/schema-standardization/`)
-   you can also specify on which branch of this repository the schema will be hosted (currently set to `neurovault`).
Then running the following should do it (if you are using python 3.7 in this case and assuming you are in the `python` directory of this repo):

```
python3.7 create_neurovault_schema.py
```

### Making the new schema available to the cobidas-ui

If the previous step went smoothly you now need to make the newly created files available on the remote of your schema-standardization repository so that the cobidas-ui repository can 'see' them. This you can do by committing the files newly created on your local schema-standardization repository and pushing them the remote. For example if the schema is hosted on the `neurovault` branch of your `origin` remote repository, the following should do the trick (assuming that you are already on the `neurovault` branch of your local repo):

```
git add --all
git commit -m 'update neurovault schema'
git push origin neurovault
```

### Rendering the checklist

Step inside the `cobidas-ui` directory, checkout the `neurovault` development branch

```
cd cobidas-ui
git checkout neurovault
```

Make sure that that you have set `cobidas-ui` correctly so it will read the schema from the right repository. This can be be set by modifying its `schema-ui/src/config.js` file (e.g see [here](https://github.com/Remi-Gau/cobidas-ui/blob/COBIDAS/src/config.js)).

You then have 2 options to run the app locally: use javascript `node.js` or use `docker`.


#### Run Locally with node.js

-   Install [node version manager](https://github.com/nvm-sh/nvm) to help you deal with different version of `node.js`.

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


#### Run locally with docker or docker-compose

Thanks to [@TimVanMourik](https://github.com/TimVanMourik) who dockerised this app in [this pull request](https://github.com/Remi-Gau/cobidas-ui/pull/2).

If you are new to docker you might want to check [this](https://the-turing-way.netlify.com/reproducible_environments/06/containers#Containers_section) first.

You can build the docker image of the app and run it with the following lines:
```
this_dir=`pwd`
docker build -t cobidas-checklist:0.0.1 .
docker run -it --rm -p 8080:8080 -v $this_dir:/code cobidas-checklist:0.0.1
```

To make things easier, can can also use [docker-compose](https://docs.docker.com/compose), which load the docker configuration from the `docker-compose.yml` file. In that case, the only things you need to do is to run:

```
docker-compose up
```
Then open your browser and go to [http://0.0.0.0:8080/](http://0.0.0.0:8080/) or [localhost:8080/](localhost:8080/)


#### Run remotely with heroku

Currently using [heroku](https://dashboard.heroku.com/apps) to  serve the app.

This can only be done on the `master` or `gh-pages` (???) fo the cobidas-ui repo. You need to set heroku as a remote repo and then push the master branch to trigger a new build of the app.

```
git push heroku master
```
