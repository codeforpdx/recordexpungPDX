import pytest
import os
import time
import datetime
import unittest

from flask import jsonify, current_app, g, request
from expungeservice.database import user
from werkzeug.security import generate_password_hash

import expungeservice


class TestUsers(unittest.TestCase):

    email = 'pytest_user@auth_test.com'
    name = 'Endpoint Test'
    group_name = 'Endpoint Test Group'
    password = 'pytest_password'

    hashed_password = generate_password_hash(password)

    def setUp(self):

        self.app = expungeservice.create_app('development')
        self.client = self.app.test_client()

        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            user.create(g.database, self.email, self.name,
                        self.group_name, self.hashed_password, False)
            expungeservice.request.teardown(None)

    def tearDown(self):
        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            expungeservice.request.teardown(None)

    def db_cleanup(self):

        cleanup_query = """DELETE FROM users where email like %(pattern)s;"""
        g.database.cursor.execute(cleanup_query, {"pattern": "%pytest%"})
        g.database.connection.commit()

    def generate_auth_token(self, email, password):
        return self.client.post('/api/auth_token', json={
            'email': email,
            'password': password,
        })

    def test_oeci_login_success(self):

        generate_auth_response = self.generate_auth_token(
            self.email, self.password)

        response = self.client.post('/api/oeci_login', headers={
            'Authorization': 'Bearer {}'.format(
                generate_auth_response.get_json()['auth_token'])},
                json={'oeci_username': "oeci_username",
                      'oeci_password': "oeci_password",
                      })

        assert(response.status_code == 201)
        assert self.client.cookie_jar._cookies[
            'localhost.local']['/']['oeci_token'].value
