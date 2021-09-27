"""
Script used to generate markdown documents that list all the
- preset response options (with link to google sheet and jsonld)
- apps (with link to google sheet, repo...)
"""

import os
from utils import get_metatable
from template_manager import TemplateManager

TemplateManager.initialize()

BASE_URL = "https://github.com/ohbm/eCOBIDAS/blob/master/"


df = get_metatable()


"""
Create file for list of response options
"""
template = TemplateManager.env.get_template("preset_response_table.j2")

response_lists = df[df["schema"].str.match(r"(^resp-.*)") == True]
files = list(response_lists["basename"])

items = []
for i in files:

    details = response_lists[response_lists["basename"] == i]

    basename = details["basename"].to_string(index=False)

    an_item = dict(
        basename=basename,
        link=details["link"].tolist()[0],
        jsonld=BASE_URL + "response_options/" + basename + ".jsonld",
    )
    items.append(an_item)

rendered_template = template.render(items=items)
with open(os.path.join("output", "preset_responses.md"), "w") as out:
    out.write(f"{rendered_template}")


"""
Create file for list of apps
"""

template = TemplateManager.env.get_template("app_table_md.j2")

apps_lists = df[df["app link"].notnull()]
apps = list(apps_lists["basename"])

items = []
# make sure to include artemis only once
artemis = False
for i in apps:

    details = apps_lists[apps_lists["basename"] == i]

    if artemis:
        continue

    dir = details["dir"].tolist()[0]
    basename = details["basename"].to_string(index=False)

    if dir == basename:
        basename = ""

    an_item = dict(
        dir=dir,
        basename=basename,
        app_link=details["app link"].tolist()[0],
        xls=details["link"].tolist()[0],
    )

    if details["repo"].any():
        an_item["repo"] = details["repo"].tolist()[0]

    if details["citation"].any():
        an_item["citation"] = details["citation"].tolist()[0]

    if an_item["dir"] == "artemis":
        artemis = True
        an_item["basename"] = ""

    items.append(an_item)


rendered_template = template.render(items=items)
with open(os.path.join("output", "apps_table.md"), "w") as out:
    out.write(f"{rendered_template}")
