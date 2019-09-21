

import unittest.mock
from unittest.mock import patch
import pytest
import os
import time
import datetime
import unittest
from werkzeug.security import generate_password_hash
from flask import jsonify, current_app, g, request

print('\n============\nTEST CASE FILE STARTING\n==============')

class MockCrawler:
    def login(self, u, p):
        print("mock crawler login")
        if u == "correct" and  p =="correct":
            return True
        else:
            return False

class TestOeciLogin(unittest.TestCase):



    email = 'pytest_user@auth_test.com'
    name = 'Endpoint Test'
    group_name = 'Endpoint Test Group'
    password = 'pytest_password'

    hashed_password = generate_password_hash(password)

    @unittest.mock.patch("expungeservice.crawler.crawler.Crawler")
    def setUp(self, mock_crawler):

        print("startings Mocked Setup")

        from expungeservice.crawler.request import URL
        from tests.fixtures.post_login_page import PostLoginPage


        from expungeservice.database import user
        import expungeservice

        from expungeservice.endpoints import oeci_login


        mock_crawler().return_value.login.return_value=False
        mock_crawler.return_value.login.return_value=False

        #crawler = expungeservice.crawler.crawler.Crawler()
        #print("in setup crawler:", crawler)


        self.app = expungeservice.create_app('development')
        self.client = self.app.test_client()

        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            user.create(g.database, self.email, self.name,
                        self.group_name, self.hashed_password, False)
            expungeservice.request.teardown(None)

    def tearDown(self):
        from expungeservice.database import user
        import expungeservice

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

    @unittest.mock.patch("expungeservice.crawler.crawler.Crawler")
    def test_oeci_login_success(self, mock_crawler):
        print("==================\ntest_oeci_login_success\n====================")

        mock_crawler.return_value.login.return_value = True
        mock_crawler().return_value.login.return_value = True


        generate_auth_response = self.generate_auth_token(
            self.email, self.password)

        response = self.client.post('/api/oeci_login', headers={
            'Authorization': 'Bearer {}'.format(
                generate_auth_response.get_json()['auth_token'])},
                json={'oeci_username': "correct",
                      'oeci_password': "correct",
                      })

        assert(response.status_code == 201)

        assert self.client.cookie_jar._cookies[
            'localhost.local']['/']['oeci_token'].value

    @unittest.mock.patch("expungeservice.crawler.crawler.Crawler")
    def test_oeci_login_invalid_credentials(self, mock_crawler):
        print("==================\ntest_oeci_login_invalid_credentials\n====================")
        mock_crawler().return_value = MockCrawler()

        mock_crawler.return_value.login.return_value = False
        print("mock_crawler.return_value.login" , mock_crawler.return_value.login)
        #mock_crawler.login = lambda u,p : (u == "username" and p == "password")
        #mock_crawler.login.return_value = True
        #mock_crawler.return_value.login.return_value = False

        #print("mock_crawler in failure:", mock_crawler)
        #input("...")

        generate_auth_response = self.generate_auth_token(
            self.email, self.password)


        response = self.client.post('/api/oeci_login', headers={
            'Authorization': 'Bearer {}'.format(
                generate_auth_response.get_json()['auth_token'])},
                json={'oeci_username': "BadUsername",
                      'oeci_password': "BadPassword",
                      })

        assert(response.status_code == 401)
