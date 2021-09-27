"""
Generates a typical landing page in english for an app
"""

import os
from utils import get_metatable
from template_manager import TemplateManager

TemplateManager.initialize()

template = TemplateManager.env.get_template("landing_page.j2")

df = get_metatable()

apps_lists = df[df["app link"].notnull()]
apps = list(apps_lists["basename"])

# TODO refactor this as it is a duplicate from app_list_tables.py
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
with open(os.path.join("output", "landing_page.html"), "w") as out:
    out.write(f"{rendered_template}")
