import pandas as pd
import pytest


@pytest.fixture
def participants_json():
    return {
        "participant_id": {"Annotations": {"IsAbout": {"TermURL": "", "Label": ""}}},
        "age": {
            "Annotations": {
                "IsAbout": {"TermURL": "nb:Age", "Label": ""},
                "Transformation": {"TermURL": "nb:FromInt", "Label": "integer data"},
                "MissingValues": ["", "n/a", " "],
            }
        },
    }


@pytest.fixture
def participants_df():
    return pd.DataFrame(
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
