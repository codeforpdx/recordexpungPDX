import importlib
import os

from flask import Flask

from .config import app_config

# Add new endpoint imports here:
from .endpoints import hello

def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])

    # Register endpoint routes here:
    hello.register(app)

    return app
