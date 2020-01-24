from http.cookiejar import Cookie

import time
import datetime

import pytest
from flask_login import login_user

from expungeservice.endpoints.auth import *


from tests.endpoints.endpoint_util import EndpointShared


@pytest.fixture
def service():
    return EndpointShared()


@pytest.fixture(autouse=True)
def setup_and_teardown(service):
    service.setup()
    yield
    service.teardown()


def test_auth_token_valid_credentials(service):
    response = service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

    assert response.status_code == 200
    assert response.headers.get("Content-type") == "application/json"
    cookie = service.client.cookie_jar._cookies["localhost.local"]["/"]["session"]
    assert cookie.version == 0
    assert cookie.name == "session"
    assert cookie.path == "/"
    assert cookie.path_specified
    assert cookie.domain == "localhost.local"
    assert not cookie.domain_specified
    assert not cookie.domain_initial_dot
    assert response.get_json()["is_admin"] is False


def test_auth_token_invalid_username(service):
    response = service.login("wrong_user@test.com", "test_password")
    assert response.status_code == 401


def test_login_invalid_pasword(service):
    response = service.login(service.user_data["user1"]["email"], "wrong_password")
    assert response.status_code == 401


def test_access_valid_auth_token(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    response = service.client.get("/api/test/user_protected")
    assert response.status_code == 200


def test_access_no_auth_token(service):
    response = service.client.get("/api/test/user_protected")
    assert response.status_code == 401


def test_access_invalid_auth_token(service):
    value = """
    .eJwljksOwyAMBe_COpHABgy5TOWv2m3SrKrevUjdzkjz3ic94vTrmY73efuWHi9LR0LjFl5yWAeSPLJ3BcMGLRBnOChDZR_UPKbU6lYWQ_Yw6BrajKP6Eky5OQQTwbKdSV0r0axD2KaKtT6xkYRAWSHMgkKIaUv35ef_DGig9YJ7UOW96uz7pDJ2WXMU4Rm0pO8PiTE6Yg.XcKUnQ.hm2dNwGedmEPV-q8FHuZvgR3Xfg
    """
    cookie = Cookie(
        version=0,
        name="session",
        value=value,
        port=None,
        port_specified=False,
        domain="localhost.local",
        domain_specified=False,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=True,
        comment=None,
        comment_url=None,
        rest={"HttpOnly": None},  # type: ignore # TODO: Clean up; this shouldn't require an ignore in theory
        rfc2109=False,
    )
    service.client.cookie_jar.set_cookie(cookie)
    response = service.client.get("/api/test/user_protected")
    assert response.status_code == 401


# We are testing the scenario in which the user's browser session has ended
# and the "remember_token" cookie has expired.
# Note the "session" cookie lasts the entire session
# (e.g. user quits browser) and has otherwise no other expiration date.
def test_access_expired_auth_token(service, monkeypatch):
    __login_user_with_custom_duration(service, monkeypatch, duration=datetime.timedelta(microseconds=1))
    service.client.cookie_jar.clear(domain="localhost.local", path="/", name="session")
    time.sleep(1)  # type: ignore
    response = service.client.get("/api/test/user_protected")
    assert response.status_code == 401

    __login_user_with_custom_duration(service, monkeypatch, duration=datetime.timedelta(days=1))
    service.client.cookie_jar.clear(domain="localhost.local", path="/", name="session")
    time.sleep(1)  # type: ignore
    response = service.client.get("/api/test/user_protected")
    assert response.status_code == 200


def __mock_login_user(duration):
    def new_login_user(user):
        return login_user(user, remember=True, duration=duration)

    return new_login_user


def __login_user_with_custom_duration(service, monkeypatch, duration):
    monkeypatch.setattr(User, "login_user", __mock_login_user(duration=duration))
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])


def test_is_admin_auth_token(service):
    login_response = service.login(service.user_data["admin"]["email"], service.user_data["admin"]["password"])
    assert login_response.get_json()["is_admin"]

    response = service.client.get("/api/test/admin_protected")
    assert response.status_code == 200

def test_is_not_admin_auth_token(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    response = service.client.get("/api/test/admin_protected")
    assert response.status_code == 403


def test_user_protected_is_unauthorized_after_logout(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    response = service.client.post("/api/logout")
    assert response.status_code == 200

    response = service.client.get("/api/test/user_protected")
    assert response.status_code == 401


# The flask-login library doesn't invalidate the "remember_token" after
# logout yet. I do not consider this a critical security flaw as
# it only is an issue if an attacker has somehow obtained the remember_token
# before the user manages to logout and clear all cookies.
def test_cookie_is_invalid_after_logout(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    cookie = service.client.cookie_jar._cookies["localhost.local"]["/"]["remember_token"]
    response = service.client.post("/api/logout")
    assert response.status_code == 200
    assert not service.client.cookie_jar._cookies["localhost.local"]["/"].get("remember_token")

    service.client.cookie_jar.clear(domain="localhost.local", path="/", name="session")
    service.client.cookie_jar.set_cookie(cookie)

    response = service.client.get("/api/test/user_protected")
    assert response.status_code == 200  # TODO: Ideally this should be 401


def test_cookie_cannot_be_used_for_fresh_login(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

    service.client.cookie_jar.clear(domain="localhost.local", path="/", name="session")

    response = service.client.put(
        "/api/users/%s" % service.user_data["user1"]["user_id"], json={"password": "new_password"}
    )
    assert response.status_code == 401
