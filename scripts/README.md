# Scripts, functions and classes to generate the eCobidas schemas

## Requirements

You will need to have python installed.

There are few dependencies (for now):

-   reproschema
-   requests_cache
-   numpy

```bash
pip install reproschema requests_cache numpy
```

If you are using conda for your environment management you should be able to
install all the dependencies with the `environment.yml` file.

```bash
conda env create --file environment.yml
```

## Generate the schemas

The highest level script that you will use to create the schema is
[convert_csv_to_schema.py](./convert_csv_to_schema.py). It will go through the
csv files in the [input folder](../inputs/csv/) and turn them into their
corresponding protocol, activity and items.

You only need to specify in the header of that script:

-   `schema_to_create` the name of the protocol you want to convert (it can be
    several of protocols at once),
-   `OUTPUT_DIR` where the schemas is meant to be created on your computer,
-   `REMOTE_REPO` the URL of the repository where the schema will be hosted

Once this is done, type this run the script from the `scripts` directory:

```bash
python create_ecobidas_schema.py
```

## Implementation

```bash
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

The core function is in [create_schema.py](./create_schema.py).

This code also relies on several classes with the classes `protocol`, `activity` and
`item` inherit from `schema`:

```bash
reproschema_schema.py
  ├── reproschema_activity.py
  ├── reproschema_item.py
  └── reproschema_protocol.py
```
