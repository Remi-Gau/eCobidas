import sys, os, json


from ..create_schema import create_schema

myPath = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, myPath + "/../")


"""
Runs the conversion of the tsv in `inputs/csv/test.tsv`
and checks that the correct jsonld are created.
"""


def test_create_schema():
    this_schema = "test"
    out_dir = os.path.join(myPath, "outputs")

    create_schema(this_schema, out_dir)

    # Check protocol
    protocol_folder = "protocols"

    output_file = os.path.join(out_dir, "tests", protocol_folder, "test_schema.jsonld")
    protocol_content = read_json(output_file)

    data_file = os.path.join(myPath, "data", protocol_folder, "test_schema.jsonld")
    expected = read_json(data_file)

    assert protocol_content == expected

    """
    CHECK ACTIVITIES
    We define the items to check for each activity below
    """
    # TODO
    # - I suspect that that this type of loop checking could be parametrized with pytest
    # - not checked: time range items
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
        {"name": "activity_4", "items": ["float_item", "multitext_item", "TEXT"]},
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

        output_file = os.path.join(
            out_dir, "tests", this_activity_folder, activity_name + "_schema.jsonld"
        )
        activity_content = read_json(output_file)

        data_file = os.path.join(
            myPath, "data", this_activity_folder, activity_name + "_schema.jsonld"
        )
        expected = read_json(data_file)

        assert activity_content == expected

        #  Check items
        item_list = activity["items"]

        for item in item_list:
            output_file = os.path.join(
                out_dir, "tests", this_activity_folder, "items", item + ".jsonld"
            )
            item_content = read_json(output_file)

            data_file = os.path.join(
                myPath, "data", this_activity_folder, "items", item + ".jsonld"
            )
            expected = read_json(data_file)

            assert item_content == expected


def read_json(file):
    with open(file, "r") as ff:
        return json.load(ff)
