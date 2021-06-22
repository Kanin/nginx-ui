from flask import Flask

from app.extensions import register_extensions
from config import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TOASTR_POSITION_CLASS"] = "toast-bottom-right"

    register_extensions(app)

    from app.ui import ui as ui_blueprint
    app.register_blueprint(ui_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
