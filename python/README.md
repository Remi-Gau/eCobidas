# Scripts, functions and classes to generate the eCobidas schemas

## Requirements and set up

You will need to have python installed.

There are few dependencies (for now). One of them is the
[`reproschema-py`](https://github.com/ReproNim/reproschema-py) package that
helps to validate that the schema you create is valid.

Preferably use a virtual environment:

```bash
virtualenv -p python3.8 env
source env/bin/activate
pip install -r requirements.txt
```

### Install the "dev" version of reproschema

```bash
# clone Rémi's fork of Reproschema on your machine, right outside of this repo
git clone https://github.com/Remi-Gau/reproschema-py.git  ../../
# checkout the "dev" branch
cd ../../reproschema-py
git checkout remi_schema_creator
# pip install it
pip install -e .
```
### Install the package

To be able to use the command line tool, do the following from within the repo

```bash
pip install -e .
```
## Generate the schemas

If you have installed the package the following command line call should run the
conversion.

```bash
ecobidas_convert    #<-- to create a whole protocol + activities
ecobidas_responses  #<-- to create a response options file
```

You only need to specify:

-   `schema` the name of the protocol you want to convert (it can be
    several of protocols at once),
-   `out_dir` where the schemas is meant to be created on your computer,
-   `repo` the URL of the repository where the schema will be hosted
-   `branch` of the repository where the schema will be hosted

### Implementation

`ecobidas_convert` calls: the highest level function that you will use to create the schema is
[create_schema.py](./create_schema.py). 

<!-- It will go through the csv files in the
[inputs folder](../../inputs/csv/) and turn them into their corresponding
protocol, activity and items. -->

Additional "entry points" should be set up in `cli.py` and adapted in `setup.py`.

This code also relies on several classes from the "dev" branch of reproschema-py:

```text
base.py               # --> Base()
  ├── protocol.py     # --> Protocol()
  ├── activity.py     # --> Activity()
  └── item.py         # --> Item(), ResponseOptions()
```

Class inheritance

```text
Base() 
  ├── Protocol()
  ├── Activity()
  ├── Item()
  └── ResponseOptions()
```  

### Validate the output

```bash
reproschema -l DEBUG validate path_to_the_file_to_validate
```

### View the results

After pushing to github:

```
https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema

https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema
```