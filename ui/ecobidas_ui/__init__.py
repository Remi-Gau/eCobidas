from logging.config import dictConfig
from pathlib import Path

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect


def create_app(test_config=None):
    from ecobidas_ui import about, auth, db, protocol

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )

    # create and configure the app
    UPLOAD_FOLDER = Path(__file__).parent / "tmp"
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

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
    bootstrap = Bootstrap5(app)  # noqa

    # Flask-WTF requires this line
    csrf = CSRFProtect(app)  # noqa

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(about.bp)
    app.register_blueprint(protocol.bp)
    app.add_url_rule("/about", endpoint="about")

    @app.route("/", methods=["GET", "POST"])
    def index() -> str:
        return render_template("index.html")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("500.html"), 500

    return app
