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

    with open(output_file, "r") as ff:
        protocol_content = json.load(ff)

    data_file = os.path.join(myPath, "data", "protocols", "test", "test_schema")

    with open(data_file, "r") as ff:
        expected = json.load(ff)

    assert protocol_content == expected
