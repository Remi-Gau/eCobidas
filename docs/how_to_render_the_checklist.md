# How the checklist is rendered

First make sure you understand how the different part of this project are organized by reading the [general organization](./general_organization.md) document.


**WARNING**

If you are trying to render the checklist and it does not work, it could mean that some of the schema references could point to URI whose content might have changed. The best in this case is to git rebase the most recent changes on the master branch on the ReproNim reproschema repository onto the branch you are trying to render.
____


## How to

### Turn the spreadsheet into the schema

This can be done by running the `create_ecobidas_schema.py` [python script](./python/create_ecobidas_schema.py) but first make sure you modify the lines in the header so that the script matches your need:
-   you will need to change the URL of the repository where the schema will be hosted (currently set to `https://raw.githubusercontent.com/Remi-Gau/reproschema/`)
-   you can also specify on which branch of this repository the schema will be hosted (currently set to `neurovault`).
Then running the following should do it (if you are using python 3.7 in this case and assuming you are in the `python` directory of this repo):

```
conda env create --file environment.yml
```

```
pip install reproschema requests_cache
```

```
python3.7 create_ecobidas_schema.py
```

python tests/jsonParser.py
reproschema -l DEBUG validate activities


### Making the new schema available to the cobidas-ui

If the previous step went smoothly you now need to make the newly created files available on the remote of your reproschema repository so that the cobidas-ui repository can 'see' them. This you can do by committing the files newly created on your local reproschema repository and pushing them the remote. For example if the schema is hosted on the `neurovault` branch of your `origin` remote repository, the following should do the trick (assuming that you are already on the `neurovault` branch of your local repo):

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
