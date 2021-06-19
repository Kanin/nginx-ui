import os


# TODO:
# Dark mode
# Do something with config
# Validate site paths
# Update README
# Reload nginx button


class Config(object):
    SECRET_KEY = "759897607520e195bf25c407330853a3"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    AUTH_PASSWORD = "supersecret"
    NGINX_PATH = "/etc/nginx"
    SITES_AVAILABLE_PATH = os.path.join(NGINX_PATH, "sites-available")
    SITES_ENABLED_PATH = os.path.join(NGINX_PATH, "sites-enabled")

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True


class WorkingConfig(Config):
    DEBUG = False


config = {
    'dev': DevConfig,
    'default': WorkingConfig
}
