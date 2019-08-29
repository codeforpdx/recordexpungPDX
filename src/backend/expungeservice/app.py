from flask import Flask

from .config import app_config

# Add new endpoint imports here:
from .endpoints import hello, auth, users
from .request import before, teardown
import logging

def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])

    log_handler = logging.StreamHandler()
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)

    # Register endpoint routes here:
    hello.register(app)
    auth.register(app)
    users.register(app)

    app.before_request(before)
    app.teardown_request(teardown)
    return app
