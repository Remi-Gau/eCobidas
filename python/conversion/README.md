# Scripts, functions and classes to generate the eCobidas schemas

## Requirements and set up

You will need to have python installed.

There are few dependencies (for now). One of them is the
[`reproschema-py`](https://github.com/ReproNim/reproschema-py) package that
helps to validate that the schema you create is valid.

```bash
pip install -r requirements.txt
```

To be able to use the command line tool, do the following

```bash
pip install -e .
```

## Generate the schemas

If you have installed the package the following command line call should run the
conversion.

```bash
convert_to_schema
```

The highest level function that you will use to create the schema is
[create_schema.py](./create_schema.py). It will go through the csv files in the
[inputs folder](../../inputs/csv/) and turn them into their corresponding
protocol, activity and items.

You only need to specify in the header of that script:

-   `schema_to_create` the name of the protocol you want to convert (it can be
    several of protocols at once),
-   `output_dir` where the schemas is meant to be created on your computer,
-   `repo` the URL of the repository where the schema will be hosted
-   `branch`

Once this is done, type this run the script from the `python` directory:

```bash
python3 cli.py
python3 create_schema.py
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
