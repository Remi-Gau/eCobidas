# Commands to use to test your schemas

To make sure they are valid JSON

```
python scripts/jsonParser.py
```

To make sure the schemas are valid

```
reproschema -l DEBUG validate protocols
reproschema -l DEBUG validate activities 
reproschema -l DEBUG validate filename
```
