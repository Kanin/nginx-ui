import os


class Config:
    # Theme
    DARK_THEME = False  # BETA: Gives the UI a darker theme

    # Auth
    AUTH_PASSWORD = "supersecret"  # Change this to the password you want to use to login
    SECRET_KEY = os.urandom(64).hex()  # The secret key flask will use, change this to keep cookie sessions

    # Pathing
    NGINX_PATH = "/etc/nginx"  # Your base NGINX path
    SITES_AVAILABLE_PATH = os.path.join(NGINX_PATH, "sites-available")  # Directory where your site files are stored
    SITES_ENABLED_PATH = os.path.join(NGINX_PATH, "sites-enabled")  # Directory where symlinks will be created for NGINX to read
