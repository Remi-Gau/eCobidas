import sys, os, json


from ..create_schema import convert_to_schema

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")


def test_convert_to_schema():

    schema_to_create = ["test"]
    output_dir = os.path.join(myPath, "outputs")
    repo = "https://raw.githubusercontent.com/Remi-Gau/eCobidas/"

    convert_to_schema(schema_to_create, output_dir, repo)

    output_file = os.path.join(output_dir, "protocols", "test", "test_schema")
    protocol_content = read_json(output_file)

    data_file = os.path.join(myPath, "data", "protocols", "test", "test_schema.jsonld")
    expected = read_json(data_file)

    assert protocol_content == expected

    output_file = os.path.join(
        output_dir, "activities", "test", "select_activity", "select_activity_schema"
    )
    activity_content = read_json(output_file)

    data_file = os.path.join(
        myPath,
        "data",
        "activities",
        "test",
        "select_activity",
        "select_activity_schema.jsonld",
    )
    expected = read_json(data_file)

    assert activity_content == expected


def read_json(file):

    with open(file, "r") as ff:
        return json.load(ff)
