from flask import Flask
from flask import current_app
from flask_login import LoginManager, UserMixin
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr
from werkzeug.security import generate_password_hash

moment = Moment()
login_manager = LoginManager()
db = SQLAlchemy()
toastr = Toastr()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5))
    password = db.Column(db.String(100))


def register_extensions(app: Flask):
    db.init_app(app)
    moment.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    toastr.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        user = User.query.filter_by(name="admin").first()
        if not user:
            db.session.add(
                User(name="admin", password=generate_password_hash(current_app.config["AUTH_PASSWORD"]))
            )
            db.session.commit()
        elif user.password != generate_password_hash(current_app.config["AUTH_PASSWORD"]):
            user.password = generate_password_hash(current_app.config["AUTH_PASSWORD"])
            db.session.commit()
