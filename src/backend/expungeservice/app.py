import pkgutil
import sys
from importlib import import_module

from flask import Flask, g
from os import path

from expungeservice.database import get_database
from .config import app_config

from . import endpoints
import logging

from .loggers import attach_logger


FRONTEND_BUILD_DIR = path.abspath(path.join(path.dirname(__file__), "..", "..", "frontend", "build"))


def before():
    g.database = get_database()


def after(response):
    g.database.connection.commit()
    return response


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__, static_folder=FRONTEND_BUILD_DIR)
    app.config.from_object(app_config[env_name])
    app.config.from_mapping(TIER=env_name)

    attach_logger(app)

    __register_endpoints(app)

    app.before_request(before)
    app.after_request(after)
    app.teardown_request(lambda exception: g.database.close_connection())

    sys.setrecursionlimit(150000)

    return app


def __register_endpoints(app):
    for _, module_name, _ in pkgutil.iter_modules(endpoints.__path__):  # type: ignore  # mypy issue #1422
        module = import_module(f"{endpoints.__name__}.{module_name}")
        register_fn = getattr(module, "register")
        register_fn(app)
