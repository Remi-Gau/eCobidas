# functions to be used by the routes
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import requests
from markupsafe import escape
from rich import print

LANG: str = "en"


def protocol_url(protocol_name: Path) -> Path:
    return (
        Path(__file__).parents[2]
        / "cobidas_schema"
        / "schemas"
        / protocol_name
        / "protocols"
        / f"{protocol_name}_schema.jsonld"
    )


@lru_cache
def get_protocol(protocol_name: str) -> dict[str, Any]:
    file = protocol_url(protocol_name)
    with open(file) as f:
        content = json.load(f)
    return content


def get_item(file: Path) -> dict[str, Any]:
    with open(file) as f:
        content = json.load(f)
    return content


@lru_cache
def query_choices(url: str) -> None | dict[str, Any]:
    try:
        data = requests.get(url).json()
    except Exception as exc:
        print(exc)
        data = None
    return data


@lru_cache
def get_landing_page(url: Path) -> None | dict[str, Any]:
    try:
        if str(url).startswith("https:"):
            data = requests.get(url)
        else:
            data = Path(url).read_text()
    except Exception as exc:
        print(exc)
        data = None
    return data


def get_nav_bar_content(
    protocol_name: str, activity_name: str | None = None
) -> list[dict[str, str]]:
    protocol_content = get_protocol(protocol_name)

    order = protocol_content["ui"]["order"]
    properties = protocol_content["ui"]["addProperties"]
    properties = sort_ui_properties(properties=properties, order=order)

    activities = [
        {"name": "Start", "link": "#", "class": "nav-link active"},
    ]
    activities.extend(
        {
            "name": activity["prefLabel"][LANG],
            "link": f"/protocol/{protocol_name}/{activity['variableName']}",
            "class": "nav-link",
        }
        for activity in properties
    )

    if activity_name:
        activities[0]["link"] = f"/protocol/{protocol_name}"
        activities[0]["class"] = "nav-link"
        for activity in activities:
            if activity["name"] == activity_name:
                activity["link"] = "#"
                activity["class"] = "nav-link active"

    return activities


def update_format(items: dict[str, Any], form):
    for i in items:
        if form[i].data:
            items[i]["is_answered"] = True
    return items


def prep_activity_page(protocol_name, activity_name):
    protocol_name = escape(protocol_name)
    activity_name = escape(activity_name)

    protocol_content = get_protocol(protocol_name)
    properties = protocol_content["ui"]["addProperties"]
    for activity in properties:
        if activity["variableName"] == activity_name:
            is_about_activity = activity["isAbout"]
            break
    activity_file = protocol_url(protocol_name).parent / is_about_activity

    with open(activity_file) as f:
        activity = json.load(f)

    activities = get_nav_bar_content(protocol_name, activity["prefLabel"][LANG])

    items = get_items_for_activity(activity_file)

    return activities, activity, items


@lru_cache
def get_items_for_activity(activity_file):
    with open(activity_file) as f:
        activity = json.load(f)

    order = activity["ui"]["order"]
    properties = activity["ui"]["addProperties"]
    properties = sort_ui_properties(properties=properties, order=order)

    items = {}
    for item in properties:

        item_name = item["variableName"]

        item_data = get_item(activity_file.parent / item["isAbout"])

        tmp = {
            "visibility": False,
            "required": False,
            "isVis": item["isVis"],
            "choices": get_choices(item_data),
            "is_answered": False,
        }

        tmp["description"] = item_data.get("description")
        tmp["question"] = item_data["question"][LANG]
        tmp["input_type"] = item_data["ui"]["inputType"]

        if item["isVis"] == 1:
            tmp["visibility"] = True

        if item["requiredValue"]:
            tmp["required"] = True

        if response_options := item_data.get("responseOptions"):
            try:
                unit = f"({response_options['unitOptions'][0]['prefLabel'][LANG]})"
            except KeyError:
                unit = ""
            tmp["unit"] = unit

            tmp["min"] = response_options.get("minValue")
            tmp["max"] = response_options.get("maxValue")

            try:
                is_multiple = response_options.get("multipleChoice", False)
            except KeyError:
                is_multiple = False
            tmp["is_multiple"] = is_multiple

        else:
            tmp["unit"] = ""
            tmp["min"] = None
            tmp["max"] = None
            tmp["is_multiple"] = None

        items[item_name] = tmp

    return items


def sort_ui_properties(properties: list[dict[str, Any]], order: list[str]) -> list[dict[str, Any]]:
    tmp = []
    for i in order:
        for prop in properties:
            if prop["isAbout"] == i:
                tmp.append(prop)
                break
    return tmp


def get_choices(item_data):
    try:
        choices = item_data["responseOptions"]["choices"]
        if isinstance(choices, str):
            choices = query_choices(choices)["choices"]
        choices = [(x["value"], x["name"][LANG]) for x in choices]
    except KeyError:
        choices = {}
    return choices
