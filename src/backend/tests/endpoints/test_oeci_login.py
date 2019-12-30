import pytest
from flask import current_app

from expungeservice.endpoints import oeci_login
from tests.endpoints.endpoint_util import EndpointShared
from expungeservice.crypto import DataCipher

@pytest.fixture
def service():
    return EndpointShared()

@pytest.fixture(autouse=True)
def setup_and_teardown(service):
    service.setup()
    with service.app.app_context():
        service.cipher = DataCipher(
            key=current_app.config.get("SECRET_KEY"))
    yield
    service.teardown()

def mock_login(value):
    return lambda s, username, password, close_session: value

def test_oeci_login_success(service, monkeypatch):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

    monkeypatch.setattr(oeci_login.Crawler, "login", mock_login(True))

    service.client.post(
        "/api/oeci_login",
        json={"oeci_username": "correctname",
              "oeci_password": "correctpwd"})

    credentials_cookie_string = service.client.cookie_jar._cookies[
        "localhost.local"]["/"]["oeci_token"].value

    creds = service.cipher.decrypt(credentials_cookie_string)

    assert creds["oeci_username"] == "correctname"
    assert creds["oeci_password"] == "correctpwd"

def test_oeci_login_invalid_credentials(service, monkeypatch):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

    monkeypatch.setattr(oeci_login.Crawler, "login", mock_login(False))

    response = service.client.post(
        "/api/oeci_login",
        json={"oeci_username": "wrongname",
              "oeci_password": "wrongpwd"})

    assert(response.status_code == 401)
