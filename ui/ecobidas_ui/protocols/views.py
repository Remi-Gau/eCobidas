import json
from pathlib import Path
from typing import Any

from ecobidas_ui.protocols.forms import (
    UploadBoldJsonForm,
    UploadParticipantsForm,
    generate_form,
    validate_participants_json,
    validate_participants_tsv,
)
from ecobidas_ui.protocols.utils import (
    LANG,
    allowed_file,
    extract_values_participants,
    get_landing_page,
    get_nav_bar_content,
    get_protocol,
    prep_activity_page,
    protocol_url,
    update_format,
)
from flask import Blueprint, current_app, flash, redirect, render_template, request
from flask_wtf import FlaskForm
from markupsafe import Markup
from werkzeug.utils import secure_filename

blueprint = Blueprint("protocol", __name__, url_prefix="/protocol")


@blueprint.route("/<protocol_name>", methods=["GET", "POST"])
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
        landing_page=landing_page,
        show_export_button=show_export_button(protocol_name),
    )


def show_export_button(protocol_name):
    return protocol_name in ["neurovault", "cobidas"]


@blueprint.get("/<protocol_name>/<activity_name>")
def activity_get(protocol_name, activity_name) -> str:

    activities, activity, items = prep_activity_page(protocol_name, activity_name)

    upload_participants_form, extra_form = generate_extra_forms(protocol_name, activity_name)

    form = generate_form(items=items, prefix=activity_name)

    completed_items = sum(bool(i["is_answered"]) for i in items.values())
    nb_items = sum(bool(i["visibility"]) for i in items.values())

    return render_template(
        "protocol.html",
        protocol_pref_label=protocol_name,
        activity_pref_label=activity["prefLabel"][LANG],
        activity_preamble=activity["preamble"][LANG],
        activities=activities,
        form=form,
        nb_items=nb_items,
        completed_items=completed_items,
        upload_participants_form=upload_participants_form,
        upload_acquisition_form=extra_form,
        show_export_button=show_export_button(protocol_name),
    )


@blueprint.post("/<protocol_name>/<activity_name>")
def activity_post(protocol_name, activity_name) -> str:
    current_app.logger.info(f"{protocol_name}-{activity_name}")

    activities, activity, items = prep_activity_page(protocol_name, activity_name)

    upload_participants_form, extra_form = generate_extra_forms(protocol_name, activity_name)

    form = generate_form(items=items, prefix=activity_name)

    if (
        upload_participants_form
        and upload_participants_form.is_submitted()
        and upload_participants_form.validate_on_submit()
    ):

        data = upload_participants_form.participants.data
        if not isinstance(data, list):
            data = [data]

        if message := validate_participants_form(data):
            flash(message, category="warning")
            return redirect(request.url)

        for file in data:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(Path(current_app.config["UPLOAD_FOLDER"]) / filename)

        tsv_file = Path(current_app.config["UPLOAD_FOLDER"]) / "participants.tsv"
        if not validate_participants_tsv(tsv_file):
            flash(
                Markup(
                    "<p>The 'participants.tsv' does not seem to be valid: 'participant_id' column is missing.</p>"
                ),
                category="warning",
            )
            return redirect(request.url)

        json_file = Path(current_app.config["UPLOAD_FOLDER"]) / "participants.json"
        if not validate_participants_json(json_file):
            flash(
                Markup(
                    "<p>The 'participants.json' was not annotated. "
                    "Annotate your data with "
                    "the <a href='https://annotate.neurobagel.org/' target='_blank'"
                    "class='alert-link'>neurobagel online annotation tool</a></p>"
                ),
                category="warning",
            )
            return redirect(request.url)

        #  TODO values in fields for participant data are not updated.
        form, items, fields = process_participants_form(
            form, activity_name, items, tsv_file, json_file
        )

        if not fields:
            message = "No field could be updated."
            flash(message, category="warning")
            return redirect(request.url)

        message = f"The following fields were updated: {fields}"
        flash(message, category="success")

    if extra_form and extra_form.is_submitted() and extra_form.validate_on_submit():

        data = extra_form.bold_json.data
        if not isinstance(data, list):
            data = [data]

        uploaded_files = []
        for file in data:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(Path(current_app.config["UPLOAD_FOLDER"]) / filename)
                uploaded_files.append(filename)
            else:
                message = "No '_bold.json' was uploaded."
                flash(message, category="warning")
                return redirect(request.url)

        form, items, fields = process_upload_form(
            form.data,
            activity_name,
            items,
            JsonMeta(Path(current_app.config["UPLOAD_FOLDER"]) / uploaded_files[0]),
        )

        if not fields:
            message = "No field could be updated."
            flash(message, category="warning")
            return redirect(request.url)

        message = f"The following fields were updated: {fields}"
        flash(message, category="success")

    elif form.is_submitted():

        form, items = update_items_and_forms(form.data, items, activity_name)

    completed_items = sum(bool(i["is_answered"]) for i in items.values())
    nb_items = sum(bool(i["visibility"]) for i in items.values())

    return render_template(
        "protocol.html",
        protocol_pref_label=protocol_name,
        activity_pref_label=activity["prefLabel"][LANG],
        activity_preamble=activity["preamble"][LANG],
        activities=activities,
        form=form,
        nb_items=nb_items,
        completed_items=completed_items,
        upload_participants_form=upload_participants_form,
        upload_acquisition_form=extra_form,
        show_export_button=show_export_button(protocol_name),
    )


def generate_extra_forms(protocol_name, activity_name) -> tuple[FlaskForm | None]:

    upload_participants_form = None
    upload_acquisition_form = None

    if protocol_name not in ["neurovault", "cobidas"]:
        return upload_participants_form, upload_acquisition_form

    if (protocol_name == "neurovault" and activity_name == "participants") or (
        protocol_name == "cobidas" and activity_name == "sample"
    ):
        upload_participants_form = UploadParticipantsForm(prefix="upload-")

    if (protocol_name == "neurovault" and activity_name == "mri_acquisition") or (
        protocol_name == "cobidas" and activity_name == "common_parameters"
    ):
        upload_acquisition_form = UploadBoldJsonForm(prefix="mri_acquisition-")

    return upload_participants_form, upload_acquisition_form


def validate_participants_form(data):
    nb_files_uploaded = len(data)
    if nb_files_uploaded != 2:
        message = f"2 files must be uploaded. Received: {nb_files_uploaded}"
        return message

    participants_json_uploaded = any(file.filename == "participants.json" for file in data)
    if not participants_json_uploaded:
        message = "No 'participants.json' was uploaded."
        return message

    participants_tsv_uploaded = any(file.filename == "participants.tsv" for file in data)
    if not participants_tsv_uploaded:
        message = "No 'participants.tsv' was uploaded."
        return message

    else:
        return ""


class JsonMeta:

    def __init__(self, json_file) -> None:
        with open(json_file) as f:
            json_content = json.load(f)
        for key in json_content:
            self.__setattr__(key, json_content[key])


def process_participants_form(form: FlaskForm, activity_name: str, items, tsv_file, json_file):
    found = extract_values_participants(tsv_file, json_content=json.load(open(json_file)))
    return process_upload_form(form.data, activity_name, items, found)


def process_upload_form(form_data, activity_name, items, found):
    form, items = update_items_and_forms(form_data, items, activity_name, obj=found)
    fields = [key for key in found.__dir__() if getattr(found, key) and key in form]
    return form, items, fields


def update_items_and_forms(form_data: dict, items, activity_name: str, obj=None):
    if obj is not None:
        for key in obj.__dir__():
            if key in form_data:
                form_data[key] = getattr(obj, key)

    items = update_visibility(items, form_data)
    items = update_format(items, form_data)
    form = generate_form(items, prefix=activity_name, obj=obj)
    return form, items


def update_visibility(items: dict[str, Any], form_data):
    """Evaluate visibility condition of each item and make item visible if necessary."""
    # assign response to a variable with same name as the item it comees from
    for key, value in form_data.items():
        if key not in items:
            continue
        if not value:
            value = None
        string_to_eval = f"{key} = {value}"
        try:
            exec(string_to_eval)
        except Exception as exc:
            current_app.logger.error(
                f"Could not execute '{string_to_eval}' as a valid python statement.\n{exc}"
            )

    # evaluate visibility
    for item, values in items.items():
        isVis = values["isVis"]
        if isinstance(isVis, str):
            try:
                items[item]["visibility"] = eval(isVis)
            except Exception as exc:
                # actually log this
                current_app.logger.error(
                    f"Could not evaluate '{eval(isVis)}' as a valid python expression.\n{exc}"
                )
                items[item]["visibility"] = False

    return items
