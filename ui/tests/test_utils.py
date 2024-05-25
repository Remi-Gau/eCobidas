import pandas as pd
from ecobidas_ui.utils import extract_values_participants


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

    assert extract_values_participants(tsv, json_content, target="number_of_subjects") == 16
    assert extract_values_participants(tsv, json_content, target="subject_age_min") == 19
    assert extract_values_participants(tsv, json_content, target="subject_age_max") == 30
    # assert mean==23.5625
