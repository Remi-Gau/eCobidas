from functools import lru_cache

import requests
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect, FlaskForm
from markupsafe import Markup, escape
from modules import activity_url, get_activity, get_item
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


class DyanmicForm(FlaskForm):
    pass


@lru_cache
def query_choices(url):
    try:
        data = requests.get(url).json()
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


@app.route("/<protocol_name>/<activity_name>", methods=["GET", "POST"])
def activity(protocol_name, activity_name):
    protocol_name = escape(protocol_name)
    activity_name = escape(activity_name)

    activity = get_activity(protocol_name, activity_name)

    items = get_items_for_activity(protocol_name, activity_name)

    form = generate_form(items)

    if form.validate_on_submit():
        for item, values in items.items():
            isVis = values["isVis"]
            if isinstance(isVis, str):
                isVis = isVis.replace(" ", "").split("==")
                if len(isVis) == 2:
                    response = form[isVis[0]].data
                    value = items[isVis[0]]["choices"].get(response)
                    expected = int(isVis[1])
                    items[item]["visibility"] = value == expected

        form = generate_form(items)

        return render_template(
            "activity.html",
            prefLabel=activity["prefLabel"][LANG],
            preamble=Markup(activity["preamble"][LANG]),
            form=form,
        )

    return render_template(
        "activity.html",
        prefLabel=activity["prefLabel"][LANG],
        preamble=Markup(activity["preamble"][LANG]),
        form=form,
    )


def generate_form(items):
    for item_name, item in items.items():

        validators = []
        if item["required"]:
            validators.append(DataRequired())

        question = f"{item['question']} {item['unit']}"

        if not item["visibility"]:
            setattr(
                DyanmicForm,
                item_name,
                HiddenField(
                    Markup(question),
                    validators=validators,
                    description=item["description"],
                ),
            )
            continue

        input_type = item["input_type"]

        if input_type not in ["select", "radio", "slider"]:

            FieldType = StringField
            if input_type == "number":
                FieldType = IntegerField
            elif input_type in ["float", "slider"]:
                FieldType = DecimalField
            elif input_type == "textarea":
                FieldType = TextAreaField

            setattr(
                DyanmicForm,
                item_name,
                FieldType(
                    Markup(question),
                    validators=validators,
                    description=item["description"],
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
                DyanmicForm,
                item_name,
                FieldType(
                    Markup(question),
                    validators=validators,
                    description=item["description"],
                    choices=[key for key in item["choices"]],
                ),
            )

    setattr(DyanmicForm, "submit", SubmitField("Submit"))  # noqa B010

    return DyanmicForm()


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
