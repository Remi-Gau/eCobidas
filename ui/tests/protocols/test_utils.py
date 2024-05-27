import pandas as pd
from ecobidas_ui.protocols.utils import (
    extract_values_participants,
    get_nav_bar_content,
    get_protocol,
    prep_activity_page,
    protocol_url,
)


def test_protocol_url():
    assert protocol_url("neurovault").suffix == ".jsonld"
    assert protocol_url("neurovault").stem == "neurovault_schema"


def test_get_protocol():
    protocol_content = get_protocol("neurovault")
    assert protocol_content["@id"] == "neurovault_schema.jsonld"


def test_get_nav_bar_content():
    nav_bar = get_nav_bar_content("neurovault", "Participants")
    assert len(nav_bar) == 9
    assert nav_bar[2]["link"] == "#"


def test_prep_activity_page():
    activities, activity, items = prep_activity_page("neurovault", "participants")


def test_extract_values_participants():
    tsv = pd.DataFrame(
        {
            "age": [
                26,
                24,
                27,
                20,
                22,
                26,
                24,
                21,
                26,
                21,
                24,
                22,
                21,
                30,
                24,
                19,
            ],
            "sex": [
                "F",
                "M",
                "F",
                "F",
                "M,",
                "F",
                "M",
                "M",
                "M",
                "F",
                "F",
                "F",
                "F",
                "F",
                "F",
                "M",
            ],
        }
    )

    json_content = {
        "age": {
            "Annotations": {
                "IsAbout": {"TermURL": "nb:Age", "Label": ""},
                "Transformation": {"TermURL": "nb:FromInt", "Label": "integer data"},
                "MissingValues": ["", "n/a", " "],
            }
        }
    }

    assert extract_values_participants(tsv, json_content).subject_age_min == 19
