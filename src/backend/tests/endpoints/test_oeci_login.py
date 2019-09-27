import base64
import cryptography
import json

from expungeservice.endpoints import oeci_login
from tests.endpoints.endpoint_util import EndpointShared


class TestOeciLogin(EndpointShared):

    def test_oeci_login_success(self):

        def faked_login(a, b, c):
            return True

    def test_oeci_login_success(self):

        oeci_login.Crawler.login = faked_login

        self.client.post(
            "/api/oeci_login", headers=self.admin_auth_header,
            json={"oeci_username": "correctname",
                  "oeci_password": "correctpwd"})

        credentials_cookie_string = self.client.cookie_jar._cookies[
            "localhost.local"]["/"]["oeci_token"].value

        jwt_key = base64.encodebytes(self.app.config.get("JWT_SECRET_KEY"))
        cipher = cryptography.fernet.Fernet(key=jwt_key)
        creds = json.loads(cipher.decrypt(bytes(
            credentials_cookie_string, "utf-8")))

        assert creds["oeci_username"] == "correctname"
        assert creds["oeci_password"] == "correctpwd"

    def test_oeci_login_invalid_credentials(self):

        def faked_login(a, b, c):
            return False

        actual_login = oeci_login.Crawler.login

        oeci_login.Crawler.login = faked_login

        response = self.client.post(
            "/api/oeci_login", headers=self.admin_auth_header,
            json={"oeci_username": "wrongname",
                  "oeci_password": "wrongpwd"})

        assert(response.status_code == 401)
