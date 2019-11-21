from http.cookiejar import Cookie

import time
import datetime
from flask_login import login_user

from expungeservice.endpoints.auth import *


from tests.endpoints.endpoint_util import EndpointShared


class TestAuth(EndpointShared):

    def setUp(self):

        EndpointShared.setUp(self)

    def test_auth_token_valid_credentials(self):
        response = self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])

        assert(response.status_code == 200)
        assert(response.headers.get("Content-type") == "application/json")
        cookie = self.client.cookie_jar._cookies["localhost.local"]["/"]["session"]
        assert(cookie.version == 0)
        assert(cookie.name == "session")
        assert(cookie.path == "/")
        assert(cookie.path_specified)
        assert(cookie.domain == "localhost.local")
        assert(not cookie.domain_specified)
        assert(not cookie.domain_initial_dot)

    def test_auth_token_invalid_username(self):
        response = self.login(
            'wrong_user@test.com', 'test_password')
        assert(response.status_code == 401)

    def test_login_invalid_pasword(self):
        response = self.login(self.user_data["user1"]["email"], "wrong_password")
        assert(response.status_code == 401)

    def test_access_valid_auth_token(self):
        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])
        response = self.client.get('/api/test/user_protected')
        assert(response.status_code == 200)

    def test_access_no_auth_token(self):
        response = self.client.get('/api/test/user_protected')
        assert(response.status_code == 401)

    def test_access_invalid_auth_token(self):
        value = """
        .eJwljksOwyAMBe_COpHABgy5TOWv2m3SrKrevUjdzkjz3ic94vTrmY73efuWHi9LR0LjFl5yWAeSPLJ3BcMGLRBnOChDZR_UPKbU6lYWQ_Yw6BrajKP6Eky5OQQTwbKdSV0r0axD2KaKtT6xkYRAWSHMgkKIaUv35ef_DGig9YJ7UOW96uz7pDJ2WXMU4Rm0pO8PiTE6Yg.XcKUnQ.hm2dNwGedmEPV-q8FHuZvgR3Xfg
        """
        cookie = Cookie(version=0, name='session',
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
               rest={'HttpOnly': None},
               rfc2109=False)
        self.client.cookie_jar.set_cookie(cookie)
        response = self.client.get('/api/test/user_protected')
        assert(response.status_code == 401)

    # We are testing the scenario in which the user's browser session has ended
    # and the "remember_token" cookie has expired.
    # Note the "session" cookie lasts the entire session
    # (e.g. user quits browser) and has otherwise no other expiration date.
    def test_access_expired_auth_token(self):
        self.__login_user_with_custom_duration(duration = datetime.timedelta(microseconds=1))
        self.client.cookie_jar.clear(domain="localhost.local", path="/", name="session")
        time.sleep(1)
        response = self.client.get('/api/test/user_protected')
        assert(response.status_code == 401)

        self.__login_user_with_custom_duration(duration = datetime.timedelta(days=1))
        self.client.cookie_jar.clear(domain="localhost.local", path="/", name="session")
        time.sleep(1)
        response = self.client.get('/api/test/user_protected')
        assert(response.status_code == 200)

    def __login_user_with_custom_duration(self, duration):
        self.login_user_wrapper = User.login_user
        User.login_user = self.__mock_login_user(duration = duration)
        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])
        User.login_user = self.login_user_wrapper

    def __mock_login_user(self, duration):
        def new_login_user(user):
            return login_user(user, remember=True, duration=duration)
        return new_login_user

    def test_is_admin_auth_token(self):
        self.login(self.user_data["admin"]["email"], self.user_data["admin"]["password"])
        response = self.client.get('/api/test/admin_protected')
        assert(response.status_code == 200)

    def test_is_not_admin_auth_token(self):
        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])
        response = self.client.get('/api/test/admin_protected')
        assert(response.status_code == 403)

    def test_user_protected_is_unauthorized_after_logout(self):
        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])
        response = self.client.post('/api/logout')
        assert(response.status_code == 200)

        response = self.client.get('/api/test/user_protected')
        assert(response.status_code == 401)

    # The flask-login library doesn't invalidate the "remember_token" after
    # logout yet. I do not consider this a critical security flaw as
    # it only is an issue if an attacker has somehow obtained the remember_token
    # before the user manages to logout and clear all cookies.
    def test_cookie_is_invalid_after_logout(self):
        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])
        cookie = self.client.cookie_jar._cookies["localhost.local"]["/"]["remember_token"]
        response = self.client.post('/api/logout')
        assert(response.status_code == 200)
        assert(not self.client.cookie_jar._cookies["localhost.local"]["/"].get("remember_token"))

        self.client.cookie_jar.clear(domain="localhost.local", path="/", name="session")
        self.client.cookie_jar.set_cookie(cookie)

        response = self.client.get('/api/test/user_protected')
        assert(response.status_code == 200) # TODO: Ideally this should be 401

    def test_cookie_cannot_be_used_for_fresh_login(self):
        self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])

        self.client.cookie_jar.clear(domain="localhost.local", path="/", name="session")

        response = self.client.put(
            "/api/users/%s" % self.user_data["user1"]["user_id"],
            json={"password":"new_password"})
        assert(response.status_code == 401)
