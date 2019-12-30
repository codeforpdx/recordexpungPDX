import pytest
from flask import current_app

from expungeservice.endpoints import oeci_login
from tests.endpoints.endpoint_util import EndpointShared
from expungeservice.crypto import DataCipher


class TestOeciLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = EndpointShared()
        self.service.setup()
        self.crawler_login = oeci_login.Crawler.login
        with self.service.app.app_context():

            self.cipher = DataCipher(
                key=current_app.config.get("SECRET_KEY"))
        yield
        oeci_login.Crawler.login = self.crawler_login
        self.service.teardown()

    def mock_login(self, value):
        return lambda s, username, password, close_session: value

    def test_oeci_login_success(self):
        self.service.login(self.service.user_data["user1"]["email"], self.service.user_data["user1"]["password"])

        oeci_login.Crawler.login = self.mock_login(True)

        self.service.client.post(
            "/api/oeci_login",
            json={"oeci_username": "correctname",
                  "oeci_password": "correctpwd"})

        credentials_cookie_string = self.service.client.cookie_jar._cookies[
            "localhost.local"]["/"]["oeci_token"].value

        creds = self.cipher.decrypt(credentials_cookie_string)

        assert creds["oeci_username"] == "correctname"
        assert creds["oeci_password"] == "correctpwd"

    def test_oeci_login_invalid_credentials(self):
        self.service.login(self.service.user_data["user1"]["email"], self.service.user_data["user1"]["password"])

        oeci_login.Crawler.login = self.mock_login(False)

        response = self.service.client.post(
            "/api/oeci_login",
            json={"oeci_username": "wrongname",
                  "oeci_password": "wrongpwd"})

        assert(response.status_code == 401)
