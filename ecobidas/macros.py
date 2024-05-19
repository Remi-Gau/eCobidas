"""Macros to help generate markdown for MkDocs.

Can be run as a script to quickly check the output.

List all the
- preset response options (with link to google sheet and jsonld)
- apps (with link to google sheet, repo...)
"""

from operator import itemgetter
from pathlib import Path

from ecobidas.template_manager import TemplateManager
from ecobidas.utils import get_spreadsheets_info


def main(output_dir: Path | None = None) -> None:
    if output_dir is None:
        output_dir = Path() / "output"
    output_dir.mkdir(exist_ok=True, parents=True)

    rendered_template = table_preset_responses()
    with open(output_dir / "preset_responses.md", "w") as out:
        out.write(f"{rendered_template}")

    rendered_template = table_apps()
    with open(output_dir / "apps_table.md", "w") as out:
        out.write(f"{rendered_template}")


def table_apps() -> str:
    """Create markdown table for list of apps."""
    spreadsheets_info = get_spreadsheets_info()
    apps = [value for key, value in spreadsheets_info.items() if spreadsheets_info[key]["app_link"]]
    apps = sorted(apps, key=itemgetter("basename"))

    TemplateManager.initialize()
    template = TemplateManager.env.get_template("app_table_md.j2")
    return template.render(apps=apps)


def table_preset_responses() -> str:
    """Create markdown table for list spreadsheets for response options."""
    BASE_URL = "https://github.com/ohbm/cobidas_schema/blob/master/"

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
