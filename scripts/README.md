# Scripts, functions and classes to generate the eCobidas schema

```
.
├── convert_csv_to_schema.py
├── create_schema.py
├── item.py
├── README.md
├── reproschema_activity.py
├── reproschema_item.py
├── reproschema_protocol.py
└── reproschema_schema.py

```

## Generate the schemas

The highest level script is
[convert_csv_to_schema.py](./convert_csv_to_schema.py) that can run through the
csv files in the [input folder](../inputs/csv/) and turn them into their
corresponding protocol, activity and items.

The core function is in [create_schema.py](./create_schema.py).

This code also relies on several classes with the classes protocol, activity and
item inherit from schema:

```
reproschema_schema.py
  ├── reproschema_activity.py
  ├── reproschema_item.py
  └── reproschema_protocol.py
```

<!-- TODO -->

This can be done by running the `create_ecobidas_schema.py`
[python script](./create_ecobidas_schema.py) but first make sure you
modify the lines in the header so that the script matches your need:

-   you will need to change the URL of the repository where the schema will be
    hosted (currently set to
    `https://raw.githubusercontent.com/Remi-Gau/reproschema/`)
-   you can also specify on which branch of this repository the schema will be
    hosted (currently set to `neurovault`). Then running the following should do
    it (if you are using python 3.7 in this case and assuming you are in the
    `python` directory of this repo):

```
conda env create --file environment.yml
```

```
pip install reproschema requests_cache
```

```
python3.7 create_ecobidas_schema.py
```