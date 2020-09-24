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

The core function is in [create_schema.py](./create_schema.pycreate_schema.py).

This code also relies on several classes with the classes protocol, activity and
item inherit from schema:

```
reproschema_schema.py
  ├── reproschema_activity.py
  ├── reproschema_item.py
  └── reproschema_protocol.py
```
