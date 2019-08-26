import pytest
import os
import time
import datetime
import unittest
from flask import jsonify, current_app, g
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from expungeservice.database import user
from expungeservice.endpoints.auth import user_auth_required, admin_auth_required


import expungeservice


'''
protected-view template endpoints.
'''
class AdminProtectedView(MethodView):
    @admin_auth_required
    def get(self):
        return 'Admin-level Protected View'
class UserProtectedView(MethodView):
            @user_auth_required
            def get(self):
                return 'User-level Protected View'


class TestAuth(unittest.TestCase):

    email = 'pytest_user@auth_test.com'
    password = 'pytest_password'
    hashed_password = generate_password_hash(password)

    def setUp(self):

        self.app = expungeservice.create_app('development')
        self.client = self.app.test_client()

        self.app.add_url_rule('/api/test/user_protected', view_func=UserProtectedView.as_view('user_protected'))
        self.app.add_url_rule('/api/test/admin_protected', view_func=AdminProtectedView.as_view('admin_protected'))

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


    def generate_auth_token(self, email, password):
        return self.client.post('/api/auth_token', json={
            'email': email,
            'password': password,
        })

    def test_auth_token_valid_credentials(self):
        response = self.generate_auth_token(self.email, self.password)

        assert(response.status_code == 200)
        assert(response.headers.get('Content-type') == 'application/json')
        data = response.get_json()
        assert('auth_token' in data)
        assert(len(data['auth_token']))

    def test_auth_token_invalid_username(self):
        response = self.generate_auth_token('wrong_user@test.com', 'test_password')
        assert(response.status_code == 401)

    def test_login_invalid_pasword(self):
        response = self.generate_auth_token(self.email, 'wrong_password')
        assert(response.status_code == 401)

    def test_access_valid_auth_token(self):
        response = self.generate_auth_token(self.email, self.password)
        response = self.client.get('/api/test/user_protected', headers={
            'Authorization': 'Bearer {}'.format(response.get_json()['auth_token'])
        })
        assert(response.status_code == 200)

    def test_access_invalid_auth_token(self):
        response = self.generate_auth_token(self.email, self.password)
        response = self.client.get('/api/test/user_protected', headers={
            'Authorization': 'Bearer {}'.format('Invalid auth token')
        })
        assert(response.status_code == 401)

    def test_access_expired_auth_token(self):
        self.app.config['JWT_EXPIRY_TIMER'] = datetime.timedelta(seconds=0)


        response = self.generate_auth_token(self.email, self.password)
        print(response)
        time.sleep(1)
        response = self.client.get('/api/test/user_protected', headers={
            'Authorization': 'Bearer {}'.format(response.get_json()['auth_token'])
        })
        assert(response.status_code == 401)

    def test_is_admin_auth_token(self):

        admin_email = 'pytest_admin_user@auth_test.com'
        admin_password = 'pytest_admin_password'
        hashed_admin_password = generate_password_hash(admin_password)

        with self.app.app_context():
            expungeservice.request.before()

            user.create_user(g.database, admin_email, hashed_admin_password, True)
            expungeservice.request.teardown(None)

        response = self.generate_auth_token(admin_email, admin_password)
        response = self.client.get('/api/test/admin_protected', headers={
            'Authorization': 'Bearer {}'.format(response.get_json()['auth_token'])
        })
        assert(response.status_code == 200)

    def test_is_not_admin_auth_token(self):

        response = self.generate_auth_token(self.email, self.password)
        response = self.client.get('/api/test/admin_protected', headers={
            'Authorization': 'Bearer {}'.format(response.get_json()['auth_token'])
        })
        assert(response.status_code == 403)
