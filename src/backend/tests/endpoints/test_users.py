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

    admin_email = 'pytest_admin@auth_test.com'
    admin_password = 'pytest_password_admin'
    admin_name = 'Endpoint AdminTest'
    admin_group_name = 'Endpoint AdminTest Group'

    hashed_admin_password = generate_password_hash(admin_password)

    def setUp(self):

        self.app = expungeservice.create_app('development')
        self.client = self.app.test_client()

        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            user.create(g.database, self.email, self.name,
                        self.group_name, self.hashed_password, False)
            user.create(g.database, self.admin_email, self.admin_name,
                        self.admin_group_name, self.hashed_admin_password,
                        True)
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

    def test_get_users_success(self):

        generate_auth_response = self.generate_auth_token(
            self.admin_email, self.admin_password)

        response = self.client.get(
            '/api/users',
            headers={
                'Authorization': 'Bearer {}'.format(
                    generate_auth_response.get_json()['auth_token'])})

        assert(response.status_code == 201)

        data = response.get_json()

        assert data['users'][0]['email']
        assert data['users'][0]['admin'] in [True, False]
        assert data['users'][0]['timestamp']
        assert data['users'][0]['name']
        assert data['users'][0]['group_name']
        assert data['users'][0]['user_id']

    def test_get_users_not_admin(self):

        generate_auth_response = self.generate_auth_token(
            self.email, self.password)

        response = self.client.get(
            '/api/users',
            headers={
                'Authorization': 'Bearer {}'.format(
                    generate_auth_response.get_json()['auth_token'])})

        assert(response.status_code == 403)
