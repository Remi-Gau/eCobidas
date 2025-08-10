"""Macros to help generate markdown for MkDocs.

Can be run as a script to quickly check the output.

List all the
- preset response options (with link to google sheet and jsonld)
- apps (with link to google sheet, repo...)
"""

import json
from operator import itemgetter
from pathlib import Path

from ecobidas.template_manager import TemplateManager
from ecobidas.utils import get_input_dir, get_spreadsheets_info

ORGA = "ohbm"
REPO = "cobidas_schema"
BRANCH = "master"
BASE_URL = f"https://github.com/{ORGA}/{REPO}/blob/{BRANCH}/"
BASE_RAW_URL = f"https://raw.githubusercontent.com/{ORGA}/{REPO}/{BRANCH}/schemas"

PREVIEW_BASE = "https://www.repronim.org/reproschema-ui/#/activities/0?url="


def main(output_dir: Path | None = None) -> None:
    if output_dir is None:
        output_dir = Path() / "output"
    output_dir.mkdir(exist_ok=True, parents=True)

    with open(output_dir / "preset_responses_table.md", "w") as out:
        out.write(f"{table_preset_responses()}")

    with open(output_dir / "apps_table.md", "w") as out:
        out.write(f"{table_apps()}")

    with open(output_dir / "spreadsheets_table.md", "w") as out:
        out.write(f"{table_spreadsheets()}")

    with open(output_dir / "data_dictionary_table.md", "w") as out:
        out.write(f"{table_data_dictionary()}")


def table_data_dictionary() -> str:
    """Create markdown table for list of apps."""
    data_dictionary_file = get_input_dir() / "data-dictionary.json"
    with open(data_dictionary_file) as f:
        data_dictionary = list(json.load(f).values())
    data_dictionary = sorted(data_dictionary, key=itemgetter("VariableName"))
    for i, _ in enumerate(data_dictionary):
        if not data_dictionary[i].get("RequirementLevel"):
            data_dictionary[i]["RequirementLevel"] = "optional"

    TemplateManager.initialize()
    template = TemplateManager.env.get_template("data_dictionary_table.j2")
    return template.render(data_dictionary=data_dictionary)


def table_spreadsheets() -> str:
    """Create markdown table for list of apps."""
    spreadsheets_info = get_spreadsheets_info()
    sheets = [
        value
        for key, value in spreadsheets_info.items()
        if (
            not value["app_link"]
            and "resp-" not in key
            and "deprecated" not in value["dir"]
            and "test" not in value["dir"]
        )
    ]
    sheets = sorted(sheets, key=itemgetter("dir"))

    for i, value in enumerate(sheets):
        if "meeg" in value["dir"]:
            continue
        sheets[i]["preview"] = (
            f"{PREVIEW_BASE}{BASE_RAW_URL}/{value['dir']}/activities/{value['basename']}/{value['basename']}_schema.jsonld"
        )

    TemplateManager.initialize()
    template = TemplateManager.env.get_template("spreadsheet_table.j2")
    return template.render(sheets=sheets)


def table_apps() -> str:
    """Create markdown table for spreadsheets that are not apps or preset responses."""
    spreadsheets_info = get_spreadsheets_info()
    apps = [value for key, value in spreadsheets_info.items() if value["app_link"]]
    apps = sorted(apps, key=itemgetter("basename"))

    TemplateManager.initialize()
    template = TemplateManager.env.get_template("app_table.j2")
    return template.render(apps=apps)


def table_preset_responses() -> str:
    """Create markdown table for list spreadsheets for response options."""
    spreadsheets_info = get_spreadsheets_info()
    responses_lists = [value for key, value in spreadsheets_info.items() if "resp-" in key]
    responses_lists = sorted(responses_lists, key=itemgetter("basename"))

    for i, value in enumerate(responses_lists):
        responses_lists[i]["jsonld"] = f"{BASE_URL}response_options/{value['basename']}.jsonld"

    TemplateManager.initialize()
    template = TemplateManager.env.get_template("preset_response_table.j2")
    return template.render(responses_lists=responses_lists)


if __name__ == "__main__":
    main()
