import os


class Config:
    # Running
    DEBUG = os.getenv("DEBUG", False)

    # Theme
    DARK_THEME = os.getenv("DARK_THEME", False)

    # Auth
    AUTH_PASSWORD = os.getenv("PASSWORD", "supersecret")
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(64).hex())

    # Pathing
    NGINX_PATH = "/hostfs/etc/nginx"
    SITES_AVAILABLE_PATH = os.path.join(NGINX_PATH, "sites-available")
    SITES_ENABLED_PATH = os.path.join(NGINX_PATH, "sites-enabled")
