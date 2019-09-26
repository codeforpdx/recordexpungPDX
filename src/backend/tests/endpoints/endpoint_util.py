import unittest
from werkzeug.security import generate_password_hash
from flask import g
from flask.views import MethodView

import expungeservice
from expungeservice.database import user
from expungeservice.endpoints.auth import *


"""
protected-view template endpoints.
"""


class AdminProtectedView(MethodView):
    @admin_auth_required
    def get(self):
        return "Admin-level Protected View"


class UserProtectedView(MethodView):
            @user_auth_required
            def get(self):
                return "User-level Protected View"


class EndpointShared(unittest.TestCase):

    email = "pytest_user@auth_test.com"
    name = "Endpoint Test"
    group_name = "Endpoint Test Group"
    password = "pytest_password"

    hashed_password = generate_password_hash(password)

    admin_email = "pytest_admin@auth_test.com"
    admin_password = "pytest_password_admin"
    admin_name = "Endpoint AdminTest"
    admin_group_name = "Endpoint AdminTest Group"

    ids = {}

    hashed_admin_password = generate_password_hash(admin_password)

    def setUp(self):

        self.app = expungeservice.create_app("development")
        self.client = self.app.test_client()

        self.app.add_url_rule(
            "/api/test/user_protected", view_func=UserProtectedView.as_view(
                "user_protected"))
        self.app.add_url_rule(
            "/api/test/admin_protected", view_func=AdminProtectedView.as_view(
                "admin_protected"))

        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            create_result = user.create(
                g.database, self.email, self.name,
                self.group_name, self.hashed_password, False)
            self.ids[self.email] = create_result["user_id"]
            create_result = user.create(
                g.database, self.admin_email, self.admin_name,
                self.admin_group_name, self.hashed_admin_password, True)
            self.ids[self.admin_email] = create_result["user_id"]
            expungeservice.request.teardown(None)

        generate_auth_response = self.generate_auth_token(
            self.email, self.password)

        self.user_auth_header = {"Authorization": "Bearer {}".format(
                generate_auth_response.get_json()["auth_token"])}

        generate_auth_response = self.generate_auth_token(
            self.admin_email, self.admin_password)

        self.admin_auth_header = {"Authorization": "Bearer {}".format(
                generate_auth_response.get_json()["auth_token"])}

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
        return self.client.post("/api/auth_token", json={
            "email": email,
            "password": password,
        })
