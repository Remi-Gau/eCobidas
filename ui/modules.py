# functions to be used by the routes
import json
from pathlib import Path


def activity_url(protocol_name, activity_name):
    return (
        Path(__file__).parents[1]
        / "cobidas_schema"
        / "schemas"
        / protocol_name
        / "activities"
        / activity_name
        / f"{activity_name}_schema.jsonld"
    )


def get_activity(protocol_name, activity_name):
    file = activity_url(protocol_name, activity_name)
    with open(file) as f:
        content = json.load(f)
    return content


def get_item(file):
    with open(file) as f:
        content = json.load(f)
    return content
