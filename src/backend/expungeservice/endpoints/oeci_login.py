import flask
from flask.views import MethodView
from flask import request, make_response, abort, jsonify
from werkzeug.security import generate_password_hash

from flask import g
from expungeservice.database import user
from expungeservice.endpoints.auth import user_auth_required
from expungeservice.request import check_data_fields
from expungeservice.request.error import error


class OeciLogin(MethodView):

    #@user_auth_required
    def post(self):
        """

        """

        data = request.get_json()

        if data is None:
            error(400, "No json data in request body")

        print("data received by OeciLogin.post():", data)
        check_data_fields(data, ['oeci_username', 'oeci_password'])

        """
        TODO: attempt login to OECI and verify credentials are correct
        """

        """
        TODO: encrypt and sign a new JWT containing the oeci credentials
        to store in the returned cookie
        """

        """
        attach a cookie  to the response object, called "oeci_token"
        """
        response = flask.make_response()
        response.set_cookie(
            "oeci_token",
            value='I\'m a fake oeci token! I don\'t expire! I\'m not secure!')


        return response, 201


def register(app):
    app.add_url_rule('/api/oeci_login', view_func=OeciLogin.as_view('oeci_login'))
