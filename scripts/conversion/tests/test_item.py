def test_get_item_info():

    from ..item import get_item_info
    import pandas as pd

    this_item = pd.DataFrame(
        {
            "visibility": ["1"],
            "mandatory": ["2"],
            "field_type": ["radio"],
            "question": ["test question"],
            "choices": ["choice A | choice B"],
            "item_pref_label": ["item name"],
        }
    )

    item_info = get_item_info(this_item)

    expected = {
        "name": "item_name",
        "item_pref_label": "item name",
        "question": "test question",
        "field_type": "radio",
        "choices": ["choice A", "choice B"],
        "visibility": True,
        "mandatory": True,
    }

    assert item_info == expected


def test_get_visibility():

    from ..item import get_visibility
    import pandas as pd

    this_item = pd.DataFrame({"visibility": ["1"]})

    # this_item = {"visibility": "1"}

    visibility = get_visibility(this_item)

    expected = True

    assert visibility == expected


def test_list_responses_options():

    from ..item import list_responses_options

    choices = list_responses_options(["A", "B"])

    print(choices)

    expected = {"choices": [], "minValue": 0, "maxValue": 2}

    expected["choices"].append({"name": "A", "value": 0, "@type": "option"})
    expected["choices"].append({"name": "B", "value": 1, "@type": "option"})
    expected["choices"].append({"name": "Other", "value": 2, "@type": "option"})

    assert choices == expected
