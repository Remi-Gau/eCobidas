"""Script used to generate markdown documents.

List all the
- preset response options (with link to google sheet and jsonld)
- apps (with link to google sheet, repo...)
"""

from pathlib import Path

from ecobidas.template_manager import TemplateManager
from ecobidas.utils import get_spreadsheets_info


def main(output_dir: Path | None = None) -> None:
    if output_dir is None:
        output_dir = Path() / "output"

    output_dir.mkdir(exist_ok=True, parents=True)

    TemplateManager.initialize()

    BASE_URL = "https://github.com/ohbm/cobidas_schema/blob/master/"

    spreadsheets_info = get_spreadsheets_info()

    """
    Create file for list of response options
    """
    template = TemplateManager.env.get_template("preset_response_table.j2")

    response_lists = {key: value for key, value in spreadsheets_info.items() if "resp-" in key}

    items = []
    for key in response_lists:
        basename = response_lists[key]["basename"]
        an_item = dict(
            basename=basename,
            link=response_lists[key]["link"],
            jsonld=f"{BASE_URL}response_options/{basename}.jsonld",
        )
        items.append(an_item)

    rendered_template = template.render(items=items)
    with open(output_dir / "preset_responses.md", "w") as out:
        out.write(f"{rendered_template}")

    """
    Create file for list of apps
    """

    template = TemplateManager.env.get_template("app_table_md.j2")

    apps_lists = {
        key: value for key, value in spreadsheets_info.items() if spreadsheets_info[key]["app_link"]
    }

    items = []
    for key in apps_lists:

        folder = apps_lists[key]["dir"]
        basename = apps_lists[key]["basename"]
        if folder == basename:
            basename = ""

        an_item = dict(
            folder=folder,
            basename=basename,
            app_link=apps_lists[key]["app_link"],
            xls=apps_lists[key]["link"],
        )

        if apps_lists[key]["repo"]:
            an_item["repo"] = apps_lists[key]["repo"]

        if apps_lists[key]["citation"]:
            an_item["citation"] = apps_lists[key]["citation"]

        items.append(an_item)

    rendered_template = template.render(items=items)
    with open(output_dir / "apps_table.md", "w") as out:
        out.write(f"{rendered_template}")


if __name__ == "__main__":
    main()
