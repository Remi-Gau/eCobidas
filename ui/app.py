import json
from pathlib import Path
from typing import Any

import pandas as pd
from flask import Flask, flash, redirect, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect, FlaskForm
from markupsafe import Markup, escape
from modules import (
    LANG,
    generate_form,
    get_items_for_activity,
    get_landing_page,
    get_nav_bar_content,
    get_protocol,
    protocol_url,
    update_format,
)
from rich import print
from werkzeug.utils import secure_filename
from wtforms import MultipleFileField, SubmitField

test_config = None

UPLOAD_FOLDER = Path(__file__).parent / "tmp"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {"tsv", "json"}

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="tO$&!|0wkamvVia0?n$NqIRVWOG",
    DATABASE=Path(app.instance_path) / "flaskr.sqlite",
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH=16 * 1000 * 1000,
)

if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile("config.py", silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
Path(app.instance_path).mkdir(parents=True, exist_ok=True)

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)

# Flask-WTF requires this line
csrf = CSRFProtect(app)


def update_visibility(items: dict[str, Any], form):
    for item, values in items.items():
        isVis = values["isVis"]
        if isinstance(isVis, str):
            isVis = isVis.replace(" ", "").split("==")
            if len(isVis) > 2:
                app.logger.warning("More than 1 '=='")
            if len(isVis) < 2:
                app.logger.warning(f"Unsupported JavaScript expression: {isVis}")
            if len(isVis) == 2 and form[isVis[0]].data:
                response = int(form[isVis[0]].data)
                expected = int(isVis[1])
                items[item]["visibility"] = response == expected
    return items


@app.route("/protocol/<protocol_name>", methods=["GET", "POST"])
def protocol(protocol_name: str) -> str:

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


@app.route("/protocol/<protocol_name>/<activity_name>", methods=["GET", "POST"])
def activity(protocol_name, activity_name) -> str:

    protocol_name = escape(protocol_name)
    activity_name = escape(activity_name)

    protocol_content = get_protocol(protocol_name)
    properties = protocol_content["ui"]["addProperties"]
    for activity in properties:
        if activity["variableName"] == activity_name:
            is_about_activity = activity["isAbout"]
            break
    activity_file = protocol_url(protocol_name).parent / is_about_activity

    upload_form = None
    if protocol_name == "neurovault" and activity_name == "participants":
        upload_form = UploadForm()

    with open(activity_file) as f:
        activity = json.load(f)

    activities = get_nav_bar_content(protocol_name, activity["prefLabel"][LANG])

    items = get_items_for_activity(activity_file)

    form = generate_form(items=items, prefix=activity_name)

    if request.method == "POST":

        if upload_form.is_submitted():

            if len(upload_form.participants.data) != 2:
                flash("2 files must be uploaded.")
                return redirect(request.url)
            if all(file.filename != "participants.json" for file in upload_form.participants.data):
                flash("No 'participants.json' was uploaded.")
                return redirect(request.url)
            if all(file.filename != "participants.tsv" for file in upload_form.participants.data):
                flash("No 'participants.tsv' was uploaded.")
                return redirect(request.url)

            for file in upload_form.participants.data:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(Path(app.config["UPLOAD_FOLDER"]) / filename)

            participants_tsv = pd.read_csv(
                Path(app.config["UPLOAD_FOLDER"]) / "participants.tsv", sep="\t"
            )
            with open(Path(app.config["UPLOAD_FOLDER"]) / "participants.json") as f:
                participants_json = json.load(f)

            if not participants_json.get("participant_id") or not participants_json[
                "participant_id"
            ].get("Annotations"):
                flash(
                    Markup(
                        "The 'participants.json' was not annotated. "
                        "Annotate your data with "
                        "the <a href='https://annotate.neurobagel.org/' class='alert-link'>neurobagel online annotation tool</a>"
                    )
                )
                return redirect(request.url)

            print(participants_tsv)
            print(participants_json)

        elif form.is_submitted():

            items = update_visibility(items, form)

            items = update_format(items, form)

            form = generate_form(items, prefix=activity_name)

            completed_items = sum(bool(i["is_answered"]) for i in items.values())
            nb_items = sum(bool(i["visibility"]) for i in items.values())

            return render_template(
                "protocol.html",
                protocol_pref_label=protocol_name,
                activity_pref_label=activity["prefLabel"][LANG],
                activity_preamble=Markup(activity["preamble"][LANG]),
                activities=activities,
                form=form,
                nb_items=nb_items,
                completed_items=completed_items,
                upload_form=upload_form,
            )

    completed_items = sum(bool(i["is_answered"]) for i in items.values())
    nb_items = sum(bool(i["visibility"]) for i in items.values())

    return render_template(
        "protocol.html",
        protocol_pref_label=protocol_name,
        activity_pref_label=activity["prefLabel"][LANG],
        activity_preamble=Markup(activity["preamble"][LANG]),
        activities=activities,
        form=form,
        nb_items=nb_items,
        completed_items=completed_items,
        upload_form=upload_form,
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    return render_template("index.html")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadForm(FlaskForm):
    participants = MultipleFileField("Upload participants.tsv and participants.json")
    submit = SubmitField("Upload")


@app.route("/about")
def about() -> str:
    return render_template("about.html")


@app.route("/new")
def new() -> str:
    return render_template("new_checklist.html")


# keep this as is
if __name__ == "__main__":
    app.run(debug=True)
