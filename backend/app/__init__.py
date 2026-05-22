import os
import logging
import traceback

from flask import Flask

from app.routes import session

from app.services.config import manage_configs
from app.services.session import SessionController

from app.core.dialogs import select_directory_dialog
from app.core.paths import STATIC_PATH, TEMPLATES_PATH
from app.core.logging import Logger


def create_app():
    log = logging.getLogger("werkzeug")
    log.disabled = True

    app = Flask(
        __name__,
        template_folder=TEMPLATES_PATH,
        static_folder=STATIC_PATH
    )

    app.secret_key = os.environ.get(
        "SECRET_KEY",
        os.urandom(24)
    )

    initialize_services(app)
    register_blueprints(app)

    return app

def initialize_services(app):
    try:
        config_path = select_directory_dialog("Select Configuration Folder")
        app.config["config_path"] = config_path
        configs = manage_configs(config_path)
        session_controller = SessionController(configs)
        app.extensions["session_controller"] = session_controller
        app.config["participant_data_file"] = config_path / "participant_data" / "participant_data.csv"
    except Exception as e:
        Logger.fail(f"{e}. {traceback.format_exc()}")
        raise

def register_blueprints(app):
    app.register_blueprint(
        session,
        url_prefix="/session"
    )