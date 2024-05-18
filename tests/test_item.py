import pandas as pd
import pytest
from reproschema.models.item import Item, ResponseOption

from ecobidas.item import (
    define_choices,
    get_item_info,
    get_visibility,
    list_responses_options,
    set_item_name,
    slider_response,
)


def test_slider_response():
    choices = ["1", "4", "4"]

    response_options = slider_response(choices)

    assert len(response_options.choices) == 4
    assert response_options.choices[1]["value"] == 1
    assert response_options.minValue == 0
    assert response_options.maxValue == 3


def test_preset():
    field_type = "radio"
    choices = ["preset:boolean"]

    item = Item()
    item.set_defaults()

    item = define_choices(item, field_type, choices)

    assert (
        item.response_options.choices
        == "https://raw.githubusercontent.com/ohbm/cobidas_schema/master/response_options/boolean.jsonld"
    )


@pytest.mark.parametrize(
    "input, expected",
    [
        ("_i[t]em-n:a m!e", "_item-na_me"),  # alphanumeric with _ and - only
        ("item name", "item_name"),
    ],
)
def test_set_item_name(input, expected):
    this_item = pd.DataFrame({"item_pref_label": [input]})

    name = set_item_name(this_item)

    assert name == expected


@pytest.mark.parametrize(
    "item_name, pref_label, expected",
    [("", "item name", "item_name"), ("foo Bar", "item name", "foo_Bar")],
)
def test_set_item_name_pref_label(item_name, pref_label, expected):
    this_item = pd.DataFrame({"item": [item_name], "item_pref_label": [pref_label]})

    name = set_item_name(this_item)

    assert name == expected


def test_get_item_info():
    this_item = pd.DataFrame(
        {
            "visibility": ["previous_item == 2"],
            "item": [""],
            "mandatory": ["1"],
            "field_type": ["radio"],
            "question": ["test question"],
            "choices": ["choice A | choice B"],
            "item_pref_label": ["item name"],
            "item_description": "",
        }
    )

    item_info = get_item_info(this_item)

    expected = {
        "name": "item_name",
        "pref_label": "item name",
        "question": "test question",
        "field_type": "radio",
        "details": "",
        "unit": "",
        "choices": ["choice A", "choice B"],
        "visibility": "previous_item == 2",
        "mandatory": True,
        "description": "item name",
        "sub_section": "",
    }

    assert item_info == expected


def test_get_item_info_with_name():
    this_item = pd.DataFrame(
        {
            "visibility": ["1"],
            "mandatory": ["2"],
            "field_type": ["radio"],
            "question": ["test question"],
            "choices": ["choice A | choice B"],
            "item_pref_label": ["item name"],
            "item": ["TEST"],
            "item_description": ["desc"],
        }
    )

    item_info = get_item_info(this_item)

    expected = {
        "name": "TEST",
        "pref_label": "item name",
        "question": "test question",
        "field_type": "radio",
        "details": "",
        "unit": "",
        "choices": ["choice A", "choice B"],
        "visibility": True,
        "mandatory": True,
        "description": "desc",
        "sub_section": "",
    }

    assert item_info == expected


def test_get_item_info_with_only_name():
    this_item = pd.DataFrame(
        {
            "visibility": ["1"],
            "mandatory": ["2"],
            "field_type": ["radio"],
            "question": ["test question"],
            "choices": ["choice A | choice B"],
            "item": ["TEST_1"],
            "item_description": ["desc"],
        }
    )

    item_info = get_item_info(this_item)

    expected = {
        "name": "TEST_1",
        "pref_label": "TEST 1",
        "question": "test question",
        "details": "",
        "unit": "",
        "field_type": "radio",
        "choices": ["choice A", "choice B"],
        "visibility": True,
        "mandatory": True,
        "description": "desc",
        "sub_section": "",
    }

    assert item_info == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (float("nan"), True),
        ("1", True),
        (1, True),
        ("0", False),
        (0, False),
        ("javascript expression", "javascript expression"),
    ],
)
def test_get_visibility(input, expected):
    this_item = pd.DataFrame({"visibility": [input]})
    visibility = get_visibility(this_item)
    assert visibility == expected


def test_list_responses_options():
    response_options = list_responses_options(["A", "B", "C"])

    expected = ResponseOption()
    expected.add_choice("A", 0)
    expected.add_choice("B", 1)
    expected.add_choice("C", 2)
    expected.set_max(2)

    assert response_options.choices == expected.choices
