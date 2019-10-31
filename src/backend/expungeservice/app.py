import pkgutil
from importlib import import_module

from flask import Flask

from .config import app_config

from . import endpoints
from .request import before, after, teardown
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

    __register_endpoints(app)

    app.before_request(before)
    app.after_request(after)
    app.teardown_request(teardown)

    app.logger.debug("Flask app created!")

    return app

def __register_endpoints(app):
    prefix = "expungeservice.endpoints."
    for _, module_name, _ in pkgutil.iter_modules(endpoints.__path__):
        module = import_module(prefix + module_name)
        register_fn = getattr(module, "register")
        register_fn(app)