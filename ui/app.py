from functools import lru_cache
from pathlib import Path

import requests
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect, FlaskForm
from markupsafe import Markup, escape
from modules import activity_url, get_activity, get_item, get_protocol, protocol_url
from rich import print
from wtforms import (
    DecimalField,
    HiddenField,
    IntegerField,
    MultipleFileField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired

LANG = "en"

app = Flask(__name__)
app.secret_key = "tO$&!|0wkamvVia0?n$NqIRVWOG"

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)

# Flask-WTF requires this line
csrf = CSRFProtect(app)


@lru_cache
def query_choices(url):
    try:
        data = requests.get(url).json()
    except Exception as exc:
        print(exc)
        data = None
    return data


@lru_cache
def get_landing_page(url: Path):
    try:
        if str(url).startswith("https:"):
            data = requests.get(url)
        else:
            with open(url) as f:
                data = f.read()
    except Exception as exc:
        print(exc)
        data = None
    return data


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/new")
def new():
    return render_template("new_checklist.html")


@app.route("/protocol/<protocol_name>", methods=["GET", "POST"])
def protocol(protocol_name):

    protocol_content = get_protocol(protocol_name)

    landing_page_url = protocol_url(protocol_name).parent / protocol_content["landingPage"]["@id"]
    landing_page = get_landing_page(landing_page_url)

    activities = get_nav_bar_content(protocol_name)

    return render_template(
        "protocol.html",
        protocol_pref_label=protocol_name,
        protocol_preamble=protocol_content["preamble"][LANG],
        activities=activities,
        landing_page=Markup(landing_page),
    )


def get_nav_bar_content(protocol_name, activity_name=None):
    protocol_content = get_protocol(protocol_name)
    activities = [
        {"name": "Start", "link": "#"},
    ]
    activities.extend(
        {
            "name": activity["prefLabel"][LANG],
            "link": f"/protocol/{protocol_name}/{activity['variableName']}",
        }
        for activity in protocol_content["ui"]["addProperties"]
    )
    if activity_name:
        activities[0]["link"] = f"/protocol/{protocol_name}"
        for activity in activities:
            if activity["name"] == activity_name:
                activity["link"] = "#"
    return activities


@app.route("/protocol/<protocol_name>/<activity_name>", methods=["GET", "POST"])
def activity(protocol_name, activity_name):

    protocol_name = escape(protocol_name)
    activity_name = escape(activity_name)

    activity = get_activity(protocol_name, activity_name)

    activities = get_nav_bar_content(protocol_name, activity["prefLabel"][LANG])

    items = get_items_for_activity(protocol_name, activity_name)

    if request.method == "POST":

        form = generate_form(form=None, items=items, prefix=activity_name)

        if form.validate_on_submit():

            items = update_visbility(items, form)

            form = generate_form(items)

            return render_template(
                "protocol.html",
                protocol_pref_label=protocol_name,
                activity_pref_label=activity["prefLabel"][LANG],
                activity_preamble=Markup(activity["preamble"][LANG]),
                activities=activities,
                form=form,
            )

    form = generate_form(form=None, items=items, prefix=activity_name)

    return render_template(
        "protocol.html",
        protocol_pref_label=protocol_name,
        activity_pref_label=activity["prefLabel"][LANG],
        activity_preamble=Markup(activity["preamble"][LANG]),
        activities=activities,
        form=form,
    )


def update_visbility(items, form):
    for item, values in items.items():
        isVis = values["isVis"]
        if isinstance(isVis, str):
            isVis = isVis.replace(" ", "").split("==")
            if len(isVis) > 2:
                app.logger.warning("More than 1 '=='")
            if len(isVis) < 2:
                app.logger.warning(f"Unsupported JavaScript expression: {isVis}")
            if len(isVis) == 2:
                response = form[isVis[0]].data
                value = items[isVis[0]]["choices"].get(response)
                expected = int(isVis[1])
                items[item]["visibility"] = value == expected
    return items


def generate_form(form=None, items=None, prefix=None):

    class DyanmicForm(FlaskForm):
        pass

    if form is None:
        form = DyanmicForm

    for item_name, item in items.items():

        validators = []
        if item["required"]:
            validators.append(DataRequired())

        question = f"{item['question']} {item['unit']}"

        if not item["visibility"]:
            setattr(
                form,
                item_name,
                HiddenField(
                    Markup(question),
                    validators=validators,
                    description=item["description"],
                    _prefix=prefix,
                ),
            )
            continue

        input_type = item["input_type"]

        default = None

        if input_type not in ["select", "radio", "slider"]:

            FieldType = StringField
            if input_type == "number":
                FieldType = IntegerField
                default = 0
            elif input_type in ["float", "slider"]:
                FieldType = DecimalField
                default = 0
            elif input_type == "textarea":
                FieldType = TextAreaField

            setattr(
                form,
                item_name,
                FieldType(
                    Markup(question),
                    validators=validators,
                    description=item["description"],
                    default=default,
                    _prefix=prefix,
                ),
            )

        else:

            is_multiple = item["is_multiple"]

            if is_multiple:
                FieldType = MultipleFileField
            if input_type == "select":
                FieldType = SelectField
            elif input_type == "radio":
                FieldType = RadioField

            setattr(
                form,
                item_name,
                FieldType(
                    Markup(question),
                    validators=validators,
                    description=item["description"],
                    choices=[key for key in item["choices"]],
                    _prefix=prefix,
                ),
            )

    setattr(form, "submit", SubmitField("Submit"))  # noqa B010

    return form()


def get_items_for_activity(protocol_name, activity_name):
    # TODO make sure items are presented in the right order
    activity = get_activity(protocol_name, activity_name)
    items = {}
    for item in activity["ui"]["addProperties"]:

        item_name = item["variableName"]

        item_data = get_item(activity_url(protocol_name, activity_name).parent / item["isAbout"])

        tmp = {
            "visibility": False,
            "required": False,
            "isVis": item["isVis"],
            "choices": get_choices(item_data),
        }

        tmp["description"] = item_data.get("description")
        tmp["question"] = item_data["question"][LANG]
        tmp["input_type"] = item_data["ui"]["inputType"]

        if item["isVis"] == 1:
            tmp["visibility"] = True

        if item["requiredValue"]:
            tmp["required"] = True

        try:
            unit = f"({item_data['responseOptions']['unitOptions'][0]['prefLabel'][LANG]})"
        except KeyError:
            unit = ""
        tmp["unit"] = unit

        try:
            is_multiple = item_data["responseOptions"].get("multipleChoice", False)
        except KeyError:
            is_multiple = False
        tmp["is_multiple"] = is_multiple

        items[item_name] = tmp

    return items


def get_choices(item_data):
    try:
        choices = item_data["responseOptions"]["choices"]
        if isinstance(choices, str):
            choices = query_choices(choices)["choices"]
        choices = {x["name"][LANG]: x["value"] for x in choices}
    except KeyError:
        choices = {}
    return choices


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# keep this as is
if __name__ == "__main__":
    app.run(debug=True)
