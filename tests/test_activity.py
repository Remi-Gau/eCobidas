import pandas as pd

from ecobidas.create_schema import make_preamble


def test_make_preamble():
    items = pd.DataFrame({"preamble": ["this is the preamble"], "item": ["TEST_1"]})

    schema_info = {
        "citation": "citation",
        "repo": "github_repo",
        "link": "google_sheet",
    }

    preamble = make_preamble(schema_info, items)

    expected = (
        "<p>"
        + "<a href='google_sheet' target='_blank' > Source </a> | "
        + "<a href='github_repo' target='_blank' > GitHub repository </a> | "
        + "<a href='citation' target='_blank' > Reference </a>"
        + "<br><br>"
        + "this is the preamble"
        + "</p>"
    )

    assert preamble == expected
