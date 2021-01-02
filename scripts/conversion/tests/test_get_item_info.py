def test_get_item_info():
    """test get item info"""
    from ..item import get_item_info

    csv_info = {
        "item": {"col": 0, "name": "do not skip"},
        "include": {"col": 1},
        "question": {"col": 2},
        "resp_type": {"col": 3},
        "choice": {"col": 4},
        "preamble": {"col": 5},
        "mandatory": {"col": 6},
        "vis": {"col": 7},
    }

    row = [
        "item_name",
        "1",  # include
        "test question",
        "radio",
        "choice A | choice B",
        "no preamble",
        "1",  # mandatory
        "1",  # visibility
    ]

    item_info = get_item_info(row, csv_info)

    print(item_info)

    expected = {
        "name": "item_name",
        "question": "test question",
        "resp_type": "radio",
        "choices": ["choice A", "choice B"],
        "visibility": True,
        "preamble": 5,
        "mandatory": True,
    }

    assert item_info == expected
