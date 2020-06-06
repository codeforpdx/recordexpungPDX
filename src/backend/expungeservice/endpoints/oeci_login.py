import requests
from flask.views import MethodView
from flask import request, make_response, current_app
import time
import os

from expungeservice.crawler.crawler import Crawler, InvalidOECIUsernamePassword, OECIUnavailable
from expungeservice.request import check_data_fields
from expungeservice.request import error
from expungeservice.crypto import DataCipher


class OeciLogin(MethodView):
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
        credentials = {"oeci_username": data["oeci_username"], "oeci_password": data["oeci_password"]}
        crawler_session = requests.Session()
        try:
            Crawler.attempt_login(crawler_session, credentials["oeci_username"], credentials["oeci_password"])
        except InvalidOECIUsernamePassword as e:
            error(401, str(e))
        except OECIUnavailable as e:
            error(404, str(e))
        finally:
            crawler_session.close()
        cipher = DataCipher(key=current_app.config.get("SECRET_KEY"))
        encrypted_credentials = cipher.encrypt(credentials)
        response = make_response()
        # TODO: We will need an OECILogout endpoint to remove httponly=true cookies from frontend
        response.set_cookie(
            "oeci_token",
            secure=os.getenv("TIER") == "production",
            httponly=False,
            samesite="strict",
            expires=time.time() + 2 * 60 * 60,  # type: ignore # 2 hour lifetime
            value=encrypted_credentials,
        )
        return response, 201


def register(app):
    app.add_url_rule("/api/oeci_login", view_func=OeciLogin.as_view("oeci_login"))
