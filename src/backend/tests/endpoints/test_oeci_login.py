import pytest
from flask import current_app

from expungeservice.crawler.crawler import InvalidOECIUsernamePassword
from expungeservice.endpoints import oeci_login
from tests.endpoints.endpoint_util import EndpointShared
from expungeservice.crypto import DataCipher


@pytest.fixture
def service():
    return EndpointShared()


@pytest.fixture(autouse=True)
def setup_and_teardown(service):
    with service.app.app_context():
        service.cipher = DataCipher(key=current_app.config.get("SECRET_KEY"))
    yield


def mock_login(value):
    return lambda s, username, password: value


def mock_login_failure(_, __, ___):
    raise InvalidOECIUsernamePassword()


def test_oeci_login_success(service, monkeypatch):
    monkeypatch.setattr(oeci_login.Crawler, "attempt_login", mock_login("Successful login response"))
    service.client.post("/api/oeci_login", json={"oeci_username": "correctname", "oeci_password": "correctpwd"})
    credentials_cookie_string = None
    for cookie in service.client.cookie_jar:
        if cookie.name == "oeci_token":
            credentials_cookie_string = cookie.value
            break
    creds = service.cipher.decrypt(credentials_cookie_string)
    assert creds["oeci_username"] == "correctname"
    assert creds["oeci_password"] == "correctpwd"


def test_oeci_login_invalid_credentials(service, monkeypatch):
    monkeypatch.setattr(oeci_login.Crawler, "attempt_login", mock_login_failure)
    response = service.client.post("/api/oeci_login", json={"oeci_username": "wrongname", "oeci_password": "wrongpwd"})
    assert response.status_code == 401
