import pytest
import os
import time
import datetime
import unittest

from flask import jsonify, current_app, g, request
from werkzeug.security import generate_password_hash

import expungeservice
from tests.endpoints.endpoint_util import EndpointShared


class TestUser(EndpointShared):

    def test_create_success(self):

        new_email = "pytest_create_user@endpoint_test.com"
        new_password = "new_password"
        new_hashed_password = generate_password_hash(new_password)

        response = self.client.post(
            "/api/user", headers=self.admin_auth_header,
            json={"email": new_email,
                  "password": new_password,
                  "name": self.name,
                  "group_name": self.group_name,
                  "admin": True})

        assert(response.status_code == 201)

        data = response.get_json()
        assert data["user_id"]
        assert data["email"] == new_email
        assert data["name"] == self.name
        assert data["group_name"] == self.group_name
        assert data["admin"] is True
        assert data["timestamp"]

    def test_create_no_auth(self):

        new_email = "pytest_create_user@endpoint_test.com"
        new_password = "new_password"

        response = self.client.post(
            "/api/user",
            headers={
                "Authorization": ""},
            json={
                "email": new_email,
                "name": self.name,
                "group_name": self.group_name,
                "password": new_password,
                "admin": False})

    def test_create_missing_data_field(self):

        new_email = "pytest_create_user@endpoint_test.com"

        generate_auth_response = self.generate_auth_token(
            self.admin_email, self.admin_password)

        response = self.client.post(
            "/api/user",
            headers=self.admin_auth_header,
            json={"email": new_email,
                  "name": self.name,
                  "group_name": self.group_name,
                  # "password": new_password,
                  "admin": True})

        assert(response.status_code == 400)

    def test_create_duplicate_email(self):

        new_email = "pytest_create_user@endpoint_test.com"
        new_password = "new_password"
        new_hashed_password = generate_password_hash(new_password)

        response = self.client.post(
            "/api/user",
            headers=self.admin_auth_header,
            json={"email": new_email,
                  "name": self.name,
                  "group_name": self.group_name,
                  "password": new_password,
                  "admin": False})

        assert(response.status_code == 201)

        response = self.client.post(
            "/api/user",
            headers=self.admin_auth_header,
            json={"email": new_email,
                  "name": self.name,
                  "group_name": self.group_name,
                  "password": new_password,
                  "admin": False})

        assert(response.status_code == 422)

    def test_create_short_password(self):

        new_email = "pytest_create_user@endpoint_test.com"
        short_password = "shrt_pw"

        response = self.client.post(
            "/api/user",
            headers=self.admin_auth_header,
            json={"email": new_email,
                  "name": self.name,
                  "group_name": self.group_name,
                  "password": short_password,
                  "admin": False}
        )

        assert(response.status_code == 422)

    def test_create_not_admin(self):

        new_email = "pytest_create_user@endpoint_test.com"
        new_password = "new_password"

        response = self.client.post(
            "/api/user",
            headers=self.user_auth_header,
            json={
                "email": new_email,
                "name": self.name,
                "group_name": self.group_name,
                "password": new_password,
                "admin": False})

        assert(response.status_code == 403)
