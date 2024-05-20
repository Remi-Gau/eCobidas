from pathlib import Path

import pytest

from ecobidas.utils import (
    get_input_dir,
    get_input_file,
    get_landing_page,
    get_output_dir,
    get_schema_info,
    get_spreadsheets_info,
)


@pytest.mark.parametrize(
    "this_schema", ["neurovault", get_input_dir() / "neurovault" / "neurovault.tsv"]
)
def test_get_schema_info(this_schema):
    get_schema_info(this_schema=this_schema)


@pytest.mark.parametrize("this_schema, dir, basename", [("neurovault", "neurovault", "neurovault")])
def test_get_schema_info_2(this_schema, dir, basename):
    schema_info = get_schema_info(this_schema)
    input_file = get_input_file(schema_info)

    expected = Path(__file__).parents[1] / "ecobidas" / "inputs" / dir / f"{basename}.tsv"

    assert input_file == expected


def test_get_output_dir(tmp_path):
    this_schema = Path(__file__).parent / "inputs" / "test.tsv"
    get_output_dir(this_schema, output_dir=tmp_path)


@pytest.mark.parametrize(
    "this_schema, filename",
    [
        ("neurovault", "../README_eCOBIDAS-en.html"),
        ("test", "../README_eCOBIDAS-en.md"),
        ("pet", "../README_PET-en.md"),
    ],
)
def test_get_landing_page(this_schema, filename):
    schema_info = get_schema_info(this_schema)
    landing_page = get_landing_page(schema_info)
    assert landing_page == filename


def test_get_spreadsheets_info():
    spreadsheets_info = get_spreadsheets_info()

    expected_keys = [
        "dir",
        "basename",
        "google_id",
        "link",
        "citation",
        "app_link",
        "landing_page",
        "repo",
    ]

    for key in spreadsheets_info:
        for check in expected_keys:
            assert check in spreadsheets_info[key]
