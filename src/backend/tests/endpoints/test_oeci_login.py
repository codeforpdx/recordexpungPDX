import base64
import cryptography
import json

from expungeservice.endpoints import oeci_login
from tests.endpoints.endpoint_util import EndpointShared


class TestOeciLogin(EndpointShared):

    def setUp(self):
        EndpointShared.setUp(self)
        self.login = oeci_login.Crawler.login

    def tearDown(self):
        oeci_login.Crawler.login = self.login

    def mock_login(self, value):
        return lambda a, b, c, d: value

    def test_oeci_login_success(self):

        oeci_login.Crawler.login = self.mock_login(True)

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

        oeci_login.Crawler.login = self.mock_login(False)

        response = self.client.post(
            "/api/oeci_login", headers=self.admin_auth_header,
            json={"oeci_username": "wrongname",
                  "oeci_password": "wrongpwd"})

        assert(response.status_code == 401)

