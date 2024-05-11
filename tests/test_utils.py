from pathlib import Path

import pytest

from ecobidas.utils import get_input_file, get_landing_page, get_output_dir, get_schema_info


@pytest.mark.parametrize("this_schema, dir, basename", [("neurovault", "neurovault", "neurovault")])
def test_get_schema_info(this_schema, dir, basename):
    schema_info = get_schema_info(this_schema)
    input_file = get_input_file(schema_info)

    expected = Path(__file__).parents[1] / "ecobidas" / "inputs" / "csv" / dir / f"{basename}.tsv"

    assert input_file == expected


def test_get_output_dir(tmp_path):
    this_schema = Path(__file__).parent / "inputs" / "csv" / "tests" / "test.tsv"
    get_output_dir(this_schema, out_dir=tmp_path)


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

    repo = "https://raw.githubusercontent.com/ohbm/cobidas_schema/master/landing_pages/"

    expected = repo + filename

    assert landing_page == expected
