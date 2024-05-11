"""Runs the conversion of the tsv in `inputs/csv/test.tsv` \
   and checks that the correct jsonld are created."""

import json
import os
from pathlib import Path

from ecobidas.create_schema import create_schema


def data_path():
    return Path(__file__).parent / "data"


def test_create_schema(tmp_path):
    this_schema = Path(__file__).parent / "inputs" / "csv" / "tests" / "test.tsv"

    # out_dir = Path(__file__).parent / "outputs"

    print("\n")

    create_schema(this_schema, tmp_path)

    # Check protocol
    protocol_folder = "protocols"

    output_file = tmp_path / "test" / protocol_folder / "test_schema.jsonld"
    protocol_content = read_json(output_file)

    data_file = data_path() / protocol_folder / "test_schema.jsonld"
    expected = read_json(data_file)

    assert protocol_content == expected

    """
    CHECK ACTIVITIES
    We define the items to check for each activity below
    """
    activities_folder = "activities"

    activities = [
        {
            "name": "select_activity",
            "items": [
                "radio_item",
                "radio_item_multiple_choice",
                "select_item",
                "select_item_multiple_choice",
                "mri_softwares",
                "yes_no_do_not_know",
            ],
        },
        {
            "name": "activity_4",
            "items": ["float_item", "multitext_item", "TEXT"],
        },
        {"name": "activity_3", "items": ["integer_item", "slider_item"]},
        {"name": "activity_2", "items": ["number_of_subjects"]},
        {
            "name": "visibility",
            "items": [
                "base0",
                "base1",
                "base",
                "multi_2_or_5",
                "multi_gt_5",
                "multi_lt_2",
                "radio_vis",
                "select_boolean0",
                "select_boolean1",
                "select_boolean",
            ],
        },
        # TODO year, date, country
    ]

    for activity in activities:
        activity_name = activity["name"]

        this_activity_folder = os.path.join(activities_folder, activity_name)

        output_file = tmp_path / "test" / this_activity_folder / f"{activity_name}_schema.jsonld"
        activity_content = read_json(output_file)
        data_file = data_path() / this_activity_folder / f"{activity_name}_schema.jsonld"
        expected = read_json(data_file)

        assert activity_content == expected

        #  Check items
        item_list = activity["items"]

        for item in item_list:
            output_file = tmp_path / "test" / this_activity_folder / "items" / f"{item}.jsonld"
            item_content = read_json(output_file)
            data_file = data_path() / this_activity_folder / "items" / f"{item}.jsonld"
            expected = read_json(data_file)

            assert item_content == expected


def read_json(file):
    with open(file) as ff:
        return json.load(ff)
