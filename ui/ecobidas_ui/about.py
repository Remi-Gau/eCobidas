from flask import Blueprint, render_template

bp = Blueprint("about", __name__)


@bp.route("/about", methods=["GET", "POST"])
def about() -> str:
    return render_template("about.html")
