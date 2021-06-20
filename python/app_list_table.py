from jinja2 import Environment, PackageLoader, select_autoescape
from utils import get_metatable

from template_manager import TemplateManager

TemplateManager.initialize()

BASE_URL = "https://github.com/ohbm/eCOBIDAS/blob/master/"

template = TemplateManager.env.get_template("table_template_responses.jinja")

df = get_metatable()


"""
Create file for list of response options
"""

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
    print(an_item)
    items.append(an_item)

rendered_template = template.render(items=items)
with open("preset_responses.md", "w") as out:
    out.write("{}".format(rendered_template))
