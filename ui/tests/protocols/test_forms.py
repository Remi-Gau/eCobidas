import pandas as pd
from ecobidas_ui.protocols.forms import validate_participants_json, validate_participants_tsv


def test_validate_participants_tsv(participants_df):
    assert validate_participants_tsv(participants_df)
    assert not validate_participants_tsv(pd.DataFrame())


def test_validate_participants_json(participants_json):
    assert validate_participants_json(participants_json)
    assert not validate_participants_json({})
