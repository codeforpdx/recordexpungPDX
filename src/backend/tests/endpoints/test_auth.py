import pytest
import os
import time
import datetime
import unittest
from flask import jsonify, current_app, g
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from expungeservice.database import user
from expungeservice.endpoints.auth import *


import expungeservice
from tests.endpoints.endpoint_util import EndpointShared


class TestAuth(EndpointShared):

    def setUp(self):

        EndpointShared.setUp(self)

    def test_auth_token_valid_credentials(self):
        response = self.generate_auth_token(self.user_data["user1"]["email"], self.user_data["user1"]["password"])

        assert(response.status_code == 200)
        assert(response.headers.get("Content-type") == "application/json")
        data = response.get_json()
        assert("auth_token" in data)
        assert(len(data["auth_token"]) > 0)
        assert(data["user_id"] == self.user_data["user1"]["user_id"])

    def test_auth_token_invalid_username(self):
        response = self.generate_auth_token(
            'wrong_user@test.com', 'test_password')
        assert(response.status_code == 401)

    def test_login_invalid_pasword(self):
        response = self.generate_auth_token(self.user_data["user1"]["email"], "wrong_password")
        assert(response.status_code == 401)

    def test_access_valid_auth_token(self):
        response = self.generate_auth_token(self.user_data["user1"]["email"], self.user_data["user1"]["password"])
        response = self.client.get(
            '/api/test/user_protected',
            headers={
                'Authorization': 'Bearer {}'.format(
                    response.get_json()['auth_token'])
            })
        assert(response.status_code == 200)

    def test_access_invalid_auth_token(self):
        response = self.client.get('/api/test/user_protected', headers={
            'Authorization': 'Bearer {}'.format('Invalid auth token')
        })
        assert(response.status_code == 401)

    def test_access_expired_auth_token(self):
        self.app.config['JWT_EXPIRY_TIMER'] = datetime.timedelta(seconds=0)

        response = self.generate_auth_token(self.user_data["user1"]["email"], self.user_data["user1"]["password"])
        time.sleep(1)
        response = self.client.get(
            '/api/test/user_protected',
            headers={
                'Authorization': 'Bearer {}'.format(
                    response.get_json()['auth_token'])
            })
        assert(response.status_code == 401)

    def test_is_admin_auth_token(self):

        response = self.generate_auth_token(self.user_data["admin"]["email"], self.user_data["admin"]["password"])
        response = self.client.get(
            '/api/test/admin_protected',
            headers={
                'Authorization': 'Bearer {}'.format(
                    response.get_json()['auth_token'])
            })
        assert(response.status_code == 200)

    def test_is_not_admin_auth_token(self):

        response = self.generate_auth_token(self.user_data["user1"]["email"], self.user_data["user1"]["password"])
        response = self.client.get(
            '/api/test/admin_protected',
            headers={
                'Authorization': 'Bearer {}'.format(
                    response.get_json()['auth_token'])
            })
        assert(response.status_code == 403)

    def generate_auth_token(self, email, password):
        return self.client.post("/api/auth_token", json={
            "email": email,
            "password": password,
        })
