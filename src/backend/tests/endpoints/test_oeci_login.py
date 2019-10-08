import base64
import cryptography
import json
from flask import current_app

from expungeservice.endpoints import oeci_login
from tests.endpoints.endpoint_util import EndpointShared
from expungeservice.crypto import DataCipher


class TestOeciLogin(EndpointShared):

    def setUp(self):
        EndpointShared.setUp(self)
        self.login = oeci_login.Crawler.login
        with self.app.app_context():

            self.cipher = DataCipher(
                key=current_app.config.get("JWT_SECRET_KEY"))

    def tearDown(self):
        oeci_login.Crawler.login = self.login

    def mock_login(self, value):
        return lambda s, username, password, close_session: value

    def test_oeci_login_success(self):

        oeci_login.Crawler.login = self.mock_login(True)

        self.client.post(
            "/api/oeci_login", headers=self.user_data["user1"]["auth_header"],
            json={"oeci_username": "correctname",
                  "oeci_password": "correctpwd"})

        credentials_cookie_string = self.client.cookie_jar._cookies[
            "localhost.local"]["/"]["oeci_token"].value

        creds = self.cipher.decrypt(credentials_cookie_string)

        assert creds["oeci_username"] == "correctname"
        assert creds["oeci_password"] == "correctpwd"

    def test_oeci_login_invalid_credentials(self):

        oeci_login.Crawler.login = self.mock_login(False)

        response = self.client.post(
            "/api/oeci_login", headers=self.user_data["user1"]["auth_header"],
            json={"oeci_username": "wrongname",
                  "oeci_password": "wrongpwd"})

        assert(response.status_code == 401)
