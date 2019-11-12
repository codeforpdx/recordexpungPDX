from flask.views import MethodView
from flask import request, make_response, current_app
import time

from expungeservice.crawler.crawler import Crawler
from expungeservice.endpoints.auth import user_auth_required
from expungeservice.request import check_data_fields
from expungeservice.request.error import error
from expungeservice.crypto import DataCipher


class OeciLogin(MethodView):

    @user_auth_required
    def post(self):
        """
        Attempts to log in to the OECI web site using the provided username
        and password if successful, encrypt those credentials and return them
        in a cookie. If the credentials
        """

        data = request.get_json()

        if data is None:
            error(400, "No json data in request body")

        check_data_fields(data, ["oeci_username", "oeci_password"])

        credentials = {"oeci_username": data["oeci_username"],
                       "oeci_password": data["oeci_password"]}

        login_result = (data["oeci_username"] == "username" and
                       data["oeci_password"] == "password")

        if not login_result:
            error(401, "Invalid OECI username or password.")

        cipher = DataCipher(
            key=current_app.config.get("SECRET_KEY"))

        encrypted_credentials = cipher.encrypt(credentials)

        response = make_response()

        response.set_cookie(
            "oeci_token",
            # currently nginx/flask app are running as HTTP
            # secure=True requires HTTPS to maintain secure cookies
            # https://resources.infosecinstitute.com/securing-cookies-httponly-secure-flags/#gref
            # We will need an OECILogout endpoint to remove httponly=true cookies from frontend
            secure=False,
            httponly=False,
            samesite="strict",
            expires=time.time() + 15 * 60,  # 15 minutes
            value=encrypted_credentials)

        return response, 201


def register(app):
    app.add_url_rule('/api/oeci_login',
                     view_func=OeciLogin.as_view('oeci_login'))