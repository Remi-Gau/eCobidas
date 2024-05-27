import json
from pathlib import Path
from typing import Any

from ecobidas_ui.forms import UploadBoldJsonForm, UploadParticipantsForm, generate_form
from ecobidas_ui.utils import (
    LANG,
    allowed_file,
    extract_values_participants,
    get_landing_page,
    get_nav_bar_content,
    get_protocol,
    prep_activity_page,
    protocol_url,
    update_format,
    validate_participants_json,
    validate_participants_tsv,
)
from flask import Blueprint, current_app, flash, redirect, render_template, request
from markupsafe import Markup
from rich import print
from werkzeug.utils import secure_filename

bp = Blueprint("protocol", __name__, url_prefix="/protocol")


def update_visibility(items: dict[str, Any], form):
    """Evaluate visibility condition of each item and make item visible if necessary."""
    # assign response to a variable with same name as the item it comees from
    for key, value in form.data.items():
        if key not in items:
            continue
        if not value:
            value = None
        string_to_eval = f"{key} = {value}"
        try:
            exec(string_to_eval)
        except Exception as exc:
            print(f"Could not execute '{string_to_eval}' as a valid python statement.")
            print(exc)

    # evaluate visibility
    for item, values in items.items():
        isVis = values["isVis"]
        if isinstance(isVis, str):
            try:
                items[item]["visibility"] = eval(isVis)
            except Exception as exc:
                # actually log this
                print(f"Could not evaluate '{eval(isVis)}' as a valid python expression.")
                print(exc)
                items[item]["visibility"] = False

    return items


@bp.route("/<protocol_name>", methods=["GET", "POST"])
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
    print(protocol_name)
    if protocol_name in ["neurovault", "cobidas"]:
        return True
    else:
        return False


@bp.get("/<protocol_name>/<activity_name>")
def activity_get(protocol_name, activity_name) -> str:

    activities, activity, items = prep_activity_page(protocol_name, activity_name)

    upload_participants_form, upload_acquisition_form = generate_additional_forms(
        protocol_name, activity_name
    )

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
        upload_acquisition_form=upload_acquisition_form,
        show_export_button=show_export_button(protocol_name),
    )


@bp.post("/<protocol_name>/<activity_name>")
def activity_post(protocol_name, activity_name) -> str:

    activities, activity, items = prep_activity_page(protocol_name, activity_name)

    upload_participants_form, upload_acquisition_form = generate_additional_forms(
        protocol_name, activity_name
    )

    form = generate_form(items=items, prefix=activity_name)

    if (
        upload_participants_form
        and upload_participants_form.is_submitted()
        and upload_participants_form.participants.data
    ):

        if message := validate_participants_form(upload_participants_form):
            flash(message)
            return redirect(request.url)

        for file in upload_participants_form.participants.data:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(Path(current_app.config["UPLOAD_FOLDER"]) / filename)

        tsv_file = Path(current_app.config["UPLOAD_FOLDER"]) / "participants.tsv"
        if not validate_participants_tsv(tsv_file):
            flash(
                Markup(
                    "<p>The 'participants.tsv' does not seem to be valid: 'participant_id' column is missing.</p>"
                )
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
                )
            )
            return redirect(request.url)

        form.number_of_subjects.data = extract_values_participants(
            tsv_file, value="number_of_subjects"
        )
        form.subject_age_mean.data = extract_values_participants(tsv_file, value="subject_age_mean")
        form.subject_age_min.data = extract_values_participants(tsv_file, value="subject_age_min")
        form.subject_age_max.data = extract_values_participants(tsv_file, value="subject_age_max")

        # TODO
        form.proportion_male_subjects.data = 0.5

        items = update_visibility(items, form)
        items = update_format(items, form)
        form = generate_form(items, prefix=activity_name)

        form.number_of_subjects.data = extract_values_participants(
            tsv_file, target="number_of_subjects"
        )
        form.subject_age_mean.data = extract_values_participants(
            tsv_file, target="subject_age_mean"
        )
        form.subject_age_min.data = extract_values_participants(tsv_file, vtarget="subject_age_min")
        form.subject_age_max.data = extract_values_participants(tsv_file, target="subject_age_max")
        form.proportion_male_subjects.data = 0.5

    if upload_acquisition_form.validate_on_submit():

        f = upload_acquisition_form.bold_json.data
        filename = secure_filename(f.filename)

        if not allowed_file(filename):
            message = "No '_bold.json' was uploaded."
            flash(message)
            return redirect(request.url)

        f.save(Path(current_app.instance_path) / filename)

        with open(Path(current_app.instance_path) / filename) as f:
            bold_json = json.load(f)

        for key in bold_json:
            if key in form:
                form[key].data = bold_json[key]

        items = update_visibility(items, form)
        items = update_format(items, form)
        form = generate_form(items, prefix=activity_name)

        for key in bold_json:
            if key in form:
                form[key].data = bold_json[key]

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
        activity_preamble=activity["preamble"][LANG],
        activities=activities,
        form=form,
        nb_items=nb_items,
        completed_items=completed_items,
        upload_participants_form=upload_participants_form,
        upload_acquisition_form=upload_acquisition_form,
        show_export_button=show_export_button(protocol_name),
    )


def validate_participants_form(upload_participants_form):
    nb_files_uploaded = len(upload_participants_form.participants.data)
    participants_json_uploaded = any(
        file.filename == "participants.json" for file in upload_participants_form.participants.data
    )
    participants_tsv_uploaded = any(
        file.filename == "participants.tsv" for file in upload_participants_form.participants.data
    )

    if nb_files_uploaded != 2:
        message = "2 files must be uploaded."
    if not participants_json_uploaded:
        message = "No 'participants.json' was uploaded."
    if not participants_tsv_uploaded:
        message = "No 'participants.tsv' was uploaded."

    if nb_files_uploaded != 2 or not participants_json_uploaded or not participants_tsv_uploaded:

        return message

    else:
        return ""


def generate_additional_forms(protocol_name, activity_name):

    upload_participants_form = None
    upload_acquisition_form = None

    if protocol_name != "neurovault":
        return upload_participants_form, upload_acquisition_form

    if activity_name == "participants":
        upload_participants_form = UploadParticipantsForm(prefix="upload-")
    if activity_name == "mri_acquisition":
        upload_acquisition_form = UploadBoldJsonForm(prefix="mri_acquisition-")

    return upload_participants_form, upload_acquisition_form
