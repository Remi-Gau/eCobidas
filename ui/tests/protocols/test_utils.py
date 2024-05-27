import pytest
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


@pytest.mark.parametrize("activity_name", ["participants", "mri_acquisition"])
def test_prep_activity_page(activity_name):
    activities, activity, items = prep_activity_page("neurovault", activity_name)


def test_extract_values_participants(participants_df, participants_json):
    assert extract_values_participants(participants_df, participants_json).subject_age_min == 19
