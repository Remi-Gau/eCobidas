from ecobidas.app_list_table import main


def test_generate_table(tmp_path):
    main(tmp_path)

    assert (tmp_path / "apps_table.md").exists()
    assert (tmp_path / "preset_responses.md").exists()
