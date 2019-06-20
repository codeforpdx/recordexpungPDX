import pytest
import os
import time
import datetime
import unittest

from flask import jsonify, current_app, g
from expungeservice.database import user
from werkzeug.security import generate_password_hash

import expungeservice

class TestAuth(unittest.TestCase):

    email = 'pytest_user@auth_test.com'
    password = 'pytest_password'
    hashed_password = generate_password_hash(password)

    def setUp(self):

        self.app = expungeservice.create_app('development')
        self.client = self.app.test_client()

        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            user.create_user(g.database, self.email, self.hashed_password, False)
            expungeservice.request.teardown(None)

    def tearDown(self):
        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            expungeservice.request.teardown(None)

    def db_cleanup(self):

        cleanup_query = """DELETE FROM users where email like %(pattern)s;"""
        g.database.cursor.execute(cleanup_query, {"pattern":"%pytest%"})
        g.database.connection.commit()


    def get_auth_token(self, email, password):
        return self.client.get('/api/v0.1/auth_token', json={
            'email': email,
            'password': password,
        })

    def test_auth_token_valid_credentials(self):
        response = self.get_auth_token(self.email, self.password)

        assert(response.status_code == 200)
        assert(response.headers.get('Content-type') == 'application/json')
        data = response.get_json()
        assert('auth_token' in data)
        assert(len(data['auth_token']))

    def test_auth_token_invalid_username(self):
        response = self.get_auth_token('wrong_user@test.com', 'test_password')
        assert(response.status_code == 401)

    def test_login_invalid_pasword(self):
        response = self.get_auth_token(self.email, 'wrong_password')
        assert(response.status_code == 401)

    def test_access_valid_auth_token(self):
        response = self.get_auth_token(self.email, self.password)
        response = self.client.get('/api/v0.1/test/protected', headers={
            'Authorization': 'Bearer {}'.format(response.get_json()['auth_token'])
        })
        assert(response.status_code == 200)

    def test_access_invalid_auth_token(self):
        response = self.get_auth_token(self.email, self.password)
        response = self.client.get('/api/v0.1/test/protected', headers={
            'Authorization': 'Bearer {}'.format('Invalid auth token')
        })
        assert(response.status_code == 401)

    def test_access_expired_auth_token(self):
        self.app.config['JWT_EXPIRY_TIMER'] = datetime.timedelta(seconds=0)


        response = self.get_auth_token(self.email, self.password)
        time.sleep(1)
        response = self.client.get('/api/v0.1/test/protected', headers={
            'Authorization': 'Bearer {}'.format(response.get_json()['auth_token'])
        })
        assert(response.status_code == 401)
