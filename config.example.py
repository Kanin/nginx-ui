import os


class Config:
    DARK_THEME = False  # BETA: Gives the UI a darker theme
    SECRET_KEY = os.urandom(64).hex()  # The secret key flask will use, change this to keep cookie sessions
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"  # Don't change unless you know what you're doing
    AUTH_PASSWORD = "supersecret"  # Change this to the password you want to use to login
    NGINX_PATH = "/etc/nginx"  # Your base NGINX path
    SITES_AVAILABLE_PATH = os.path.join(NGINX_PATH, "sites-available")  # Directory where your site files are stored
    SITES_ENABLED_PATH = os.path.join(NGINX_PATH, "sites-enabled")  # Directory where symlinks will be created for NGINX to read
