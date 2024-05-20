from ecobidas.generate_landing_page import main as landing_page_main
from ecobidas.macros import main as app_list_table_main


def test_generate_table(tmp_path):
    app_list_table_main(tmp_path)
    assert (tmp_path / "apps_table.md").exists()
    assert (tmp_path / "preset_responses_table.md").exists()


def test_landing_page(tmp_path):
    landing_page_main(tmp_path)
    assert (tmp_path / "landing_page.html").exists()
