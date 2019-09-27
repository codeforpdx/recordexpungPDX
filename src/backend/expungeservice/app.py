from flask import Flask

from .config import app_config

# Add new endpoint imports here:
from .endpoints import hello, auth, users, oeci_login
from .request import before, teardown
import logging

from .loggers import attach_logger


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])

    attach_logger(app)
    app.logger.setLevel(logging.DEBUG)

    # Register endpoint routes here:
    hello.register(app)
    auth.register(app)
    users.register(app)
    oeci_login.register(app)

    app.before_request(before)
    app.teardown_request(teardown)

    app.logger.debug("Flask app created!")

    return app
