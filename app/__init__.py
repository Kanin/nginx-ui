import flask
from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_toastr import Toastr

from config import config

moment = Moment()
login_manager = LoginManager()
db = SQLAlchemy()
toastr = Toastr()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5))
    password = db.Column(db.String(100))


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    app.secret_key = app.config["SECRET_KEY"]

    config[config_name].init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    toastr.init_app(app)
    app.config["TOASTR_POSITION_CLASS"] = "toast-bottom-right"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.ui import ui as ui_blueprint
    app.register_blueprint(ui_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    with app.app_context():
        db.create_all()
        user = User.query.filter_by(name="admin").first()
        if not user:
            db.session.add(
                User(name="admin", password=generate_password_hash(flask.current_app.config["AUTH_PASSWORD"]))
            )
            db.session.commit()
        elif user.password != generate_password_hash(flask.current_app.config["AUTH_PASSWORD"]):
            user.password = generate_password_hash(flask.current_app.config["AUTH_PASSWORD"])
            db.session.commit()

    @app.errorhandler(404)
    def notfound(error):
        return flask.render_template("404.html"), 404

    return app
