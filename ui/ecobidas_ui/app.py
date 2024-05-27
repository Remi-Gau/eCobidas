import logging
import sys

from ecobidas_ui import auth, db, protocol, public
from ecobidas_ui.extensions import bootstrap, cache, csrf_protect, debug_toolbar
from ecobidas_ui.initializers.assets import init_assets
from flask import Flask, flash, render_template


def create_app(config_object="ecobidas_ui.settings"):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_object)

    register_extensions(app)
    db.init_app(app)

    init_assets(app)
    register_blueprints(app)
    register_errorhandlers(app)
    configure_logger(app)

    @app.route("/export")
    def export() -> str:
        flash("Not implemented yet!")
        return render_template("index.html")

    @app.route("/generate")
    def generate() -> str:
        flash("Not implemented yet!")
        return render_template("index.html")

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bootstrap.init_app(app)
    csrf_protect.init_app(app)
    cache.init_app(app)
    debug_toolbar.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(auth.bp)
    app.register_blueprint(protocol.bp)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
