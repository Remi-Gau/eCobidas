import sys, os, json


from ..create_schema import convert_to_schema

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")


def test_convert_to_schema():

    schema_to_create = ["test"]
    output_dir = os.path.join(myPath, "outputs")
    repo = "https://raw.githubusercontent.com/Remi-Gau/eCobidas/"

    convert_to_schema(schema_to_create, output_dir, repo)

    # check protocol
    protocol_folder = os.path.join("protocols", "test")

    output_file = os.path.join(output_dir, protocol_folder, "test_schema")
    protocol_content = read_json(output_file)

    data_file = os.path.join(myPath, "data", protocol_folder, "test_schema")
    expected = read_json(data_file)

    assert protocol_content == expected

    # check activities
    activities_folder = os.path.join("activities", "test")

    activity_name = "select_activity"
    this_activity_folder = os.path.join(activities_folder, activity_name)

    output_file = os.path.join(
        output_dir, this_activity_folder, activity_name + "_schema"
    )
    activity_content = read_json(output_file)

    data_file = os.path.join(
        myPath, "data", this_activity_folder, activity_name + "_schema"
    )
    expected = read_json(data_file)

    assert activity_content == expected

    #  Check items
    item_list = ["radio_item", "select_item"]

    for item in item_list:

        output_file = os.path.join(output_dir, this_activity_folder, "items", item)
        item_content = read_json(output_file)

        data_file = os.path.join(
            myPath,
            "data",
            this_activity_folder,
            "items",
            item,
        )
        expected = read_json(data_file)

        assert item_content == expected

    # Check activity
    activity_name = "activity_4"
    this_activity_folder = os.path.join(activities_folder, activity_name)

    # Check items
    item_list = ["float_item"]
    # "multitext_item"

    for item in item_list:

        output_file = os.path.join(output_dir, this_activity_folder, "items", item)
        item_content = read_json(output_file)

        data_file = os.path.join(
            myPath,
            "data",
            this_activity_folder,
            "items",
            item,
        )
        expected = read_json(data_file)

        assert item_content == expected

    # # Check activity
    # activity_name = "activity_3"

    # # Check items
    # item_list = ["slider_item"]

    # for item in item_list:

    #     output_file = os.path.join(output_dir, this_activity_folder, "items", item)
    #     item_content = read_json(output_file)

    #     data_file = os.path.join(
    #         myPath,
    #         "data",
    #         this_activity_folder,
    #         "items",
    #         item,
    #     )
    #     expected = read_json(data_file)

    #     assert item_content == expected


def read_json(file):

    with open(file, "r") as ff:
        return json.load(ff)
