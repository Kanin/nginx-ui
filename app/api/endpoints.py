import datetime
import os

import flask
from flask_login import login_required

from app.api import api


@api.route("/config/<name>", methods=["GET"])
@login_required
def get_config(name: str):
    """
    Reads the file with the corresponding name that was passed.

    :param name: Configuration file name
    :type name: str

    :return: Rendered HTML document with content of the configuration file.
    :rtype: str
    """
    nginx_path = flask.current_app.config["NGINX_PATH"]

    with open(os.path.join(nginx_path, name), "r") as f:
        file = f.read()

    return flask.render_template("config.html", name=name, file=file), 200


@api.route("/config/<name>", methods=["POST"])
@login_required
def post_config(name: str):
    """
    Accepts the customized configuration and saves it in the configuration file with the supplied name.

    :param name: Configuration file name
    :type name: str

    :return:
    :rtype: werkzeug.wrappers.Response
    """
    content = flask.request.get_json()
    nginx_path = flask.current_app.config["NGINX_PATH"]

    with open(os.path.join(nginx_path, name), "w") as file:
        file.write(content["file"])

    return flask.make_response({"success": True}), 200


@api.route("/domains", methods=["GET"])
@login_required
def get_domains():
    """
    Reads all files from the configuration file directory and checks the state of the site configuration.

    :return: Rendered HTML document with the domains
    :rtype: str
    """
    available_path = flask.current_app.config["SITES_AVAILABLE_PATH"]
    enabled_path = flask.current_app.config["SITES_ENABLED_PATH"]
    sites_available = []
    sites_enabled = []

    for site in os.listdir(available_path):
        available_site = os.path.join(available_path, site)
        enabled_site = os.path.join(enabled_path, site)
        if os.path.isfile(available_site):
            name = site.split(".")[0].replace("_", ".")
            time = datetime.datetime.fromtimestamp(os.path.getmtime(available_site))
            sites_available.append({
                "name": name,
                "time": time
            })
            if os.path.exists(enabled_site):
                sites_enabled.append(name)

    # sort sites by name
    sites_available = sorted(sites_available, key=lambda _site: _site["name"])
    return flask.render_template("domains.html", sites_available=sites_available, sites_enabled=sites_enabled), 200


@api.route("/domain/<name>", methods=["GET"])
@login_required
def get_domain(name: str):
    """
    Takes the name of the domain configuration file and
    returns a rendered HTML with the current configuration of the domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Rendered HTML document with the domain
    :rtype: str
    """
    name = name.replace(".", "_")
    available_path = flask.current_app.config["SITES_AVAILABLE_PATH"]
    enabled_path = flask.current_app.config["SITES_ENABLED_PATH"]
    file_data = ""
    enabled = False

    for site in os.listdir(available_path):
        available_site = os.path.join(available_path, site)
        enabled_site = os.path.join(enabled_path, site)
        if os.path.isfile(available_site) and site.startswith(name):
            name = site.split(".")[0].replace("_", ".")

            if os.path.exists(enabled_site):
                enabled = True

            with open(available_site, "r") as file_content:
                file_data = file_content.read()

            break

    return flask.render_template("domain.html", name=name, file=file_data, enabled=enabled), 200


@api.route("/domain/<name>", methods=["POST"])
@login_required
def post_domain(name: str):
    """
    Creates the configuration file of the domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """

    available_path = flask.current_app.config["SITES_AVAILABLE_PATH"]
    new_domain = flask.render_template("new_domain.j2", name=name)

    name = name.replace(".", "_") + ".conf"

    try:
        with open(os.path.join(available_path, name), "w") as file:
            file.write(new_domain)

        response = flask.jsonify({"success": True}), 201
    except OSError as ex:
        response = flask.jsonify({"success": False, "error_msg": ex}), 500

    return response


@api.route("/domain/<name>", methods=["DELETE"])
@login_required
def delete_domain(name: str):
    """
    Deletes the configuration file of the corresponding domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    name = name.replace(".", "_")
    available_path = flask.current_app.config["SITES_AVAILABLE_PATH"]
    enabled_path = flask.current_app.config["SITES_ENABLED_PATH"]
    removed = False

    for site in os.listdir(available_path):
        available_site = os.path.join(available_path, site)
        enabled_site = os.path.join(enabled_path, site)
        if os.path.isfile(available_site) and site.startswith(name):
            if os.path.exists(enabled_site):
                os.remove(enabled_site)

            os.remove(available_site)

            removed = not os.path.exists(available_site) and not os.path.exists(enabled_site)
            break

    if removed:
        return flask.jsonify({"success": True}), 200
    else:
        return flask.jsonify({"success": False}), 400


@api.route("/domain/<name>", methods=["PUT"])
@login_required
def put_domain(name: str):
    """
    Updates the configuration file with the corresponding domain name.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    name = name.replace(".", "_")
    content = flask.request.get_json()
    available_path = flask.current_app.config["SITES_AVAILABLE_PATH"]

    for site in os.listdir(available_path):
        available_site = os.path.join(available_path, site)
        if os.path.isfile(available_site) and site.startswith(name):
            with open(available_site, "w") as file:
                file.write(content["file"])

    return flask.make_response({"success": True}), 200


@api.route("/domain/<name>/enable", methods=["POST"])
@login_required
def enable_domain(name: str):
    """
    Activates the domain in Nginx so that the configuration is applied.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    name = name.replace(".", "_")
    content = flask.request.get_json()
    available_path = flask.current_app.config["SITES_AVAILABLE_PATH"]
    enabled_path = flask.current_app.config["SITES_ENABLED_PATH"]

    for site in os.listdir(available_path):
        available_site = os.path.join(available_path, site)
        enabled_site = os.path.join(enabled_path, site)
        if os.path.isfile(available_site) and site.startswith(name):
            if content["enable"]:
                if os.path.exists(enabled_site):
                    break

                os.symlink(available_site, enabled_site)
            elif os.path.exists(enabled_site):
                os.remove(enabled_site)

    return flask.make_response({"success": True}), 200
