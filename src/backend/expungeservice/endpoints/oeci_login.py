import flask
from flask.views import MethodView
from flask import request, make_response, abort, jsonify, g
from werkzeug.security import generate_password_hash
import time

print("====\n====\n====\n====\n====\n====\nOECILOGIN ENDPOINT IMPORT STARTING====\n====\n====\n====\n====\n====\n")

from expungeservice.crawler.crawler import Crawler
from expungeservice.database import user
from expungeservice.endpoints.auth import user_auth_required
from expungeservice.request import check_data_fields
from expungeservice.request.error import error

print("====\n====\n====\n====\n====\n====\nOECILOGIN ENDPOINT IMPORT HAPPENED====\n====\n====\n====\n====\n====\n")
input()

class OeciLogin(MethodView):

    @user_auth_required
    def post(self):
        """

        """

        data = request.get_json()

        if data is None:
            error(400, "No json data in request body")

        check_data_fields(data, ['oeci_username', 'oeci_password'])

        print("in oeci login endpoint, json data is:\n")
        print(data)
        c = Crawler()
        print("\ncrawler object is :\n", c)

        login_result = c.login(data["oeci_username"], data["oeci_password"])

        print("crawler.login in endpoint result:", login_result)
        input("...")

        if not login_result:
            error(401, "Invalid OECI login credentials")

        """
        TODO: encrypt and sign a new JWT containing the oeci credentials
        to store in the returned cookie
        """

        response = flask.make_response()

        response.set_cookie(
            "oeci_token",
            secure = True,
            httponly = True,
            samesite = 'strict',
            expires =  time.time() + 15 * 60,
            value="I'm a fake oeci token!")

        app = flask.Flask(__name__)

        return response, 201


def register(app):
    app.add_url_rule('/api/oeci_login', view_func=OeciLogin.as_view('oeci_login'))
