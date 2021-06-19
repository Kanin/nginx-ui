import os

import flask
from flask_login import login_required

from app.ui import ui


@ui.route("/", methods=["GET"])
@login_required
def index():
    """
    Delivers the home page of Nginx UI.

    :return: Rendered HTML document.
    :rtype: str
    """
    nginx_path = flask.current_app.config["NGINX_PATH"]
    config = [file for file in os.listdir(nginx_path) if os.path.isfile(os.path.join(nginx_path, file))]
    return flask.render_template('index.html', config=config)
