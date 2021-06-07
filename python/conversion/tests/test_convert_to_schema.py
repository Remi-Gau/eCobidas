import sys, os, json


from ..create_schema import convert_to_schema

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")


def test_convert_to_schema():

    schema_to_create = ["test"]
    output_dir = os.path.join(myPath, "outputs")
    repo = "https://raw.githubusercontent.com/Remi-Gau/eCobidas/"

    convert_to_schema(schema_to_create, output_dir, repo)

    # Check protocol
    protocol_folder = "protocols"

    output_file = os.path.join(output_dir, protocol_folder, "test_schema.jsonld")
    protocol_content = read_json(output_file)

    data_file = os.path.join(myPath, "data", protocol_folder, "test_schema.jsonld")
    expected = read_json(data_file)

    assert protocol_content == expected

    # Check activities
    activities_folder = "activities"

    # Check activity
    activities = [
        {"name": "select_activity", "items": ["radio_item", "select_item"]},
        {
            "name": "activity_4",
            "items": ["float_item"],
        },  #  "multitext_item", "text_item"
        {"name": "activity_3", "items": ["integer_item"]},  #  "slider_item"
    ]

    for activity in activities:

        activity_name = activity["name"]

        this_activity_folder = os.path.join(activities_folder, activity_name)

        output_file = os.path.join(
            output_dir, this_activity_folder, activity_name + "_schema.jsonld"
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
                output_dir, this_activity_folder, "items", item + ".jsonld"
            )
            item_content = read_json(output_file)

            data_file = os.path.join(
                myPath,
                "data",
                this_activity_folder,
                "items",
                item + ".jsonld",
            )
            expected = read_json(data_file)

            assert item_content == expected


def read_json(file):

    with open(file, "r") as ff:
        return json.load(ff)
