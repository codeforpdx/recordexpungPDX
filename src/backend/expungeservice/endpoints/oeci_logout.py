import requests
from flask.views import MethodView
from flask import request, make_response, current_app
import time
import os

from expungeservice.crawler.crawler import Crawler, InvalidOECIUsernamePassword, OECIUnavailable
from expungeservice.request import check_data_fields
from expungeservice.request import error
from expungeservice.crypto import DataCipher


class OeciLogout(MethodView):
    def post(self):
        """
        Attempts to log in to the OECI web site using the provided username
        and password if successful, encrypt those credentials and return them
        in a cookie. If the credentials
        """
        response = make_response()
        # TODO: We will need an OECILogout endpoint to remove httponly=true cookies from frontend
        response.delete_cookie("oeci_token")
        return response


def register(app):
    app.add_url_rule("/api/oeci_logout", view_func=OeciLogout.as_view("oeci_logout"))