import importlib
import os

from flask import Flask, render_template

from .config import app_config

# Add new endpoint imports here:
from .endpoints import hello
from src.frontend.blueprints.page import page
from src.backend.expungeservice.extensions import debug_toolbar 

def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    app.register_blueprint(page)

    # Register endpoint routes here:
    hello.register(app)
    extensions(app)

    return app

def extensions(app):
    # :param app: Flask Application instance
    # register extensions 
    # return: none 

    debug_toolbar.init_app(app)
    return None