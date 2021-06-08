import sys, os
import pandas as pd

from ..item import (
    get_item_info,
    get_visibility,
    define_choices,
    list_responses_options,
    slider_response,
)

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

local_reproschema = "/home/remi/github/reproschema-py/reproschema/models/"
sys.path.insert(0, local_reproschema)

from reproschema.models.item import ResponseOption, Item


def test_slider_response():

    choices = ["1", "4", "4"]

    response_options = slider_response(choices)

    assert len(response_options.options["choices"]) == 4
    assert response_options.options["choices"][1]["value"] == int(1)
    assert response_options.options["minValue"] == 0
    assert response_options.options["maxValue"] == 4


def test_preset():

    field_type = "radio"
    choices = ["preset:boolean"]

    item = Item()
    item.set_defaults()

    item = define_choices(item, field_type, choices)

    assert (
        item.response_options.options
        == "https://raw.githubusercontent.com/ohbm/eCOBIDAS/master/response_options/boolean.jsonld"
    )


def test_get_item_info():

    this_item = pd.DataFrame(
        {
            "visibility": ["1"],
            "mandatory": ["2"],
            "field_type": ["radio"],
            "question": ["test question"],
            "choices": ["choice A | choice B"],
            "item_pref_label": ["item name"],
            "item_description": ["desc"],
        }
    )

    item_info = get_item_info(this_item)

    expected = {
        "name": "item_name",
        "pref_label": "item name",
        "question": "test question",
        "field_type": "radio",
        "choices": ["choice A", "choice B"],
        "visibility": True,
        "mandatory": True,
        "description": "desc",
    }

    assert item_info == expected


def test_get_visibility():

    this_item = pd.DataFrame({"visibility": ["1"]})
    visibility = get_visibility(this_item)
    assert visibility == True

    this_item = pd.DataFrame({"visibility": [1]})
    visibility = get_visibility(this_item)
    assert visibility == True

    this_item = pd.DataFrame({"visibility": ["0"]})
    visibility = get_visibility(this_item)
    assert visibility == False

    this_item = pd.DataFrame({"visibility": [0]})
    visibility = get_visibility(this_item)
    assert visibility == False

    this_item = pd.DataFrame({"visibility": ["javascript expression"]})
    visibility = get_visibility(this_item)


def test_list_responses_options():

    response_options = list_responses_options(["A", "B", "C"])

    expected = ResponseOption()
    expected.add_choice("A", 0)
    expected.add_choice("B", 1)
    expected.add_choice("C", 2)
    expected.set_max(2)

    assert response_options.options == expected.options
