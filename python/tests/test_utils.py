import sys, os, pytest
import pandas as pd

from ..utils import get_input_file, get_schema_info, get_landing_page


@pytest.mark.parametrize(
    "this_schema, dir, basename", [("neurovault", "neurovault", "neurovault")]
)
def test_get_schema_info(this_schema, dir, basename):

    schema_info = get_schema_info(this_schema)
    input_file = get_input_file(schema_info)

    root = os.path.dirname(__file__)

    expected = os.path.abspath(
        os.path.join(root, "..", "..", "inputs", "csv", dir, basename + ".tsv")
    )

    assert input_file == expected


@pytest.mark.parametrize(
    "this_schema, filename",
    [
        ("neurovault", "README_eCOBIDAS-en.md"),
        ("test", "README_eCOBIDAS-en.md"),
        ("pet", "README_PET-en.md"),
    ],
)
def test_get_landing_page(this_schema, filename):

    schema_info = get_schema_info(this_schema)
    landing_page = get_landing_page(schema_info)

    repo = "https://raw.githubusercontent.com/ohbm/eCOBIDAS/master/landing_pages/"

    expected = repo + filename

    assert landing_page == expected
