import sys, os

from ..create_schema import convert_to_schema

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")


def test_convert_to_schema():

    schema_to_create = ["neurovault"]
    output_dir = os.path.join(myPath, "outputs")
    repo = "https://raw.githubusercontent.com/Remi-Gau/eCobidas/"

    convert_to_schema(schema_to_create, output_dir, repo)