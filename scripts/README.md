# Scripts, functions and classes to generate the eCobidas schemas

## Requirements

You will need to have python installed.

There are few dependencies (for now). One of them is the [`reproschema-py`](https://github.com/ReproNim/reproschema-py)
package that helps to validate that the schema you create is valid.

```bash
# create a new virtual environment in ecobidas
$ virtualenv --python=python3.8 ecobidas
# activate the new environment
$ source ecobidas/bin/activate
```

```bash
pip install -r requirements.txt
```

## Generate the schemas

The highest level script that you will use to create the schema is
[convert_csv_to_schema.py](./conversion/convert_csv_to_schema.py). It will go through the
csv files in the [input folder](../inputs/csv/) and turn them into their
corresponding protocol, activity and items.

You only need to specify in the header of that script:

-   `schema_to_create` the name of the protocol you want to convert (it can be
    several of protocols at once),
-   `OUTPUT_DIR` where the schemas is meant to be created on your computer,
-   `REMOTE_REPO` the URL of the repository where the schema will be hosted

Once this is done, type this run the script from the `scripts` directory:

```bash
python3 scripts/conversion/convert_csv_to_schema.py
```

### Implementation

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

This code also relies on several classes with the classes `protocol`, `activity`
and `item` inherit from `schema`:

```bash
reproschema_schema.py
  ├── reproschema_activity.py
  ├── reproschema_item.py
  └── reproschema_protocol.py
```

### Validate the output

```bash
reproschema -l DEBUG validate activities
reproschema -l DEBUG validate protocols
reproschema -l DEBUG validate path_to_the_file_to_validate
```

### View the results

After pushing to github:

```
https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema
https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema
```
