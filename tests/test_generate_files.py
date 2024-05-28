from ecobidas.macros import main as app_list_table_main


def test_generate_table(tmp_path):
    app_list_table_main(tmp_path)
    assert (tmp_path / "apps_table.md").exists()
    assert (tmp_path / "preset_responses_table.md").exists()
