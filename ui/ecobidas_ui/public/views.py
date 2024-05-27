"""Public section, including homepage and signup."""

import json

from ecobidas_ui.settings import STATIC_FOLDER
from flask import Blueprint, current_app, render_template

blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    current_app.logger.info("Hello from the home page!")
    return render_template("public/index.html")


@blueprint.route("/faq/")
def faq():
    data = json.load(open(STATIC_FOLDER / "json" / "faq.json"))
    return render_template("public/faq.html", data=data)


@blueprint.route("/about/")
def about():
    """About page."""
    return render_template("public/about.html")
