import datetime
import os
import subprocess

from flask import render_template, make_response, request, current_app, jsonify
from flask_login import login_required

from app.api import api


@api.route("/reload-nginx", methods=["POST"])
@login_required
def reload_nginx():
    res = subprocess.run("sudo nginx -t", shell=True, stderr=subprocess.PIPE)
    if res.returncode != 0:
        return make_response({"success": False, "message": str(res.stderr)}), 400
    subprocess.run("sudo nginx -s reload", shell=True)
    return make_response({"success": True}), 200


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
    nginx_path = current_app.config["NGINX_PATH"]

    with open(os.path.join(nginx_path, name), "r") as f:
        file = f.read()

    return render_template("components/config.html", name=name, file=file), 200


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
    content = request.get_json()
    nginx_path = current_app.config["NGINX_PATH"]

    with open(os.path.join(nginx_path, name), "w") as file:
        file.write(content["file"])

    return make_response({"success": True}), 200


@api.route("/sites", methods=["GET"])
@login_required
def get_sites():
    """
    Reads all files from the configuration file directory and checks the state of the site configuration.

    :return: Rendered HTML document with the sites
    :rtype: str
    """
    available_path = current_app.config["SITES_AVAILABLE_PATH"]
    enabled_path = current_app.config["SITES_ENABLED_PATH"]
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
    return render_template("components/sites.html", sites_available=sites_available, sites_enabled=sites_enabled), 200


@api.route("/site/<name>", methods=["GET"])
@login_required
def get_site(name: str):
    """
    Takes the name of the site configuration file and
    returns a rendered HTML with the current configuration of the site.

    :param name: The site name that corresponds to the name of the file.
    :type name: str

    :return: Rendered HTML document with the site
    :rtype: str
    """
    name = name.replace(".", "_")
    available_path = current_app.config["SITES_AVAILABLE_PATH"]
    enabled_path = current_app.config["SITES_ENABLED_PATH"]
    file_data = ""
    site_name = "placeholder.com"
    enabled = False

    for site in os.listdir(available_path):
        available_site = os.path.join(available_path, site)
        enabled_site = os.path.join(enabled_path, site)
        site_name = site.split(".")[0]
        if os.path.isfile(available_site) and site_name == name:
            site_name = site_name.replace("_", ".")

            if os.path.exists(enabled_site):
                enabled = True

            with open(available_site, "r") as file_content:
                file_data = file_content.read()

            break

    return render_template("components/site.html", name=site_name, file=file_data, enabled=enabled), 200


@api.route("/site/<name>", methods=["POST"])
@login_required
def post_site(name: str):
    """
    Creates the configuration file of the site.

    :param name: The site name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """

    available_path = current_app.config["SITES_AVAILABLE_PATH"]
    new_site = render_template("components/new_site.j2", name=name)

    name = name.replace(".", "_") + ".conf"
    if os.path.isfile(os.path.join(available_path, name)):
        return jsonify(success=False, message="That site already exists!"), 409

    try:
        with open(os.path.join(available_path, name), "w") as file:
            file.write(new_site)

        response = jsonify(success=True), 201
    except OSError as error:
        response = jsonify(success=False, message=error), 500

    return response


@api.route("/site/<name>", methods=["DELETE"])
@login_required
def delete_site(name: str):
    """
    Deletes the configuration file of the corresponding site.

    :param name: The site name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    name = name.replace(".", "_")
    available_path = current_app.config["SITES_AVAILABLE_PATH"]
    enabled_path = current_app.config["SITES_ENABLED_PATH"]
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
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 400


@api.route("/site/<name>", methods=["PUT"])
@login_required
def put_site(name: str):
    """
    Updates the configuration file with the corresponding site name.

    :param name: The site name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    name = name.replace(".", "_")
    content = request.get_json()
    available_path = current_app.config["SITES_AVAILABLE_PATH"]

    for site in os.listdir(available_path):
        available_site = os.path.join(available_path, site)
        if os.path.isfile(available_site) and site.startswith(name):
            with open(available_site, "w") as file:
                file.write(content["file"])

    return make_response({"success": True}), 200


@api.route("/site/<name>/enable", methods=["POST"])
@login_required
def enable_site(name: str):
    """
    Activates the site in Nginx so that the configuration is applied.

    :param name: The site name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    name = name.replace(".", "_")
    content = request.get_json()
    available_path = current_app.config["SITES_AVAILABLE_PATH"]
    enabled_path = current_app.config["SITES_ENABLED_PATH"]

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

    return make_response({"success": True}), 200
