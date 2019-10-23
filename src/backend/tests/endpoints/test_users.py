import pytest
import os
import time
import datetime
import unittest
import copy

from flask import jsonify, current_app, g, request
from werkzeug.security import generate_password_hash

import expungeservice
from tests.endpoints.endpoint_util import EndpointShared


class TestUsers(EndpointShared):

    def setUp(self):
        EndpointShared.setUp(self)

        self.user_data["new_user"] = {
            "email": "pytest_create_user@endpoint_test.com",
            "password": "new_password",
            "hashed_password": generate_password_hash("new_password"),
            "name": "new name",
            "group_name": "new group name",
            "admin": False
        }

    def check_user_data_match(self, created_user, reference_user):
        assert created_user["email"] == reference_user["email"]
        assert created_user["name"] == reference_user["name"]
        assert created_user["group_name"] == reference_user["group_name"]
        assert created_user["admin"] == reference_user["admin"]
        assert created_user["timestamp"]

    def test_create_success(self):



        response = self.client.post(
            "/api/users", headers=self.user_data["admin"]["auth_header"],
            json=self.user_data["new_user"])

        assert(response.status_code == 201)

        data = response.get_json()
        self.check_user_data_match(data, self.user_data["new_user"])



    def test_create_no_auth(self):

        response = self.client.post(
            "/api/users",
            headers={
                "Authorization": ""},
            json=self.user_data["new_user"])

    def test_create_missing_data_field(self):

        response = self.client.post(
            "/api/users",
            headers=self.user_data["admin"]["auth_header"],
            json={"email": self.user_data["new_user"]["email"],
                  "name": self.user_data["new_user"]["name"],
                  "group_name": self.user_data["new_user"]["group_name"],
                  # "password": new_password,
                  "admin": True})

        assert(response.status_code == 400)

    def test_create_duplicate_email(self):

        response = self.client.post(
            "/api/users",
            headers=self.user_data["admin"]["auth_header"],
            json=self.user_data["new_user"])

        assert(response.status_code == 201)

        response = self.client.post(
            "/api/users",
            headers=self.user_data["admin"]["auth_header"],
            json=self.user_data["new_user"])

        assert(response.status_code == 422)

    def test_create_short_password(self):

        new_email = "pytest_create_user@endpoint_test.com"
        short_password = "shrt_pw"

        response = self.client.post(
            "/api/users",
            headers=self.user_data["admin"]["auth_header"],
            json={"email": self.user_data["new_user"]["email"],
                  "name": self.user_data["new_user"]["name"],
                  "group_name": self.user_data["new_user"]["group_name"],
                  "password": short_password,
                  "admin": False}
        )

        assert(response.status_code == 422)

    def test_create_not_admin(self):

        new_email = "pytest_create_user@endpoint_test.com"
        new_password = "new_password"

        response = self.client.post(
            "/api/users",
            headers=self.user_data["user1"]["auth_header"],
            json=self.user_data["new_user"])

        assert(response.status_code == 403)

    def test_get_users_success(self):

        response = self.client.get(
            "/api/users",
            headers=self.user_data["admin"]["auth_header"])

        assert(response.status_code == 201)

        data = response.get_json()

        assert data["users"][0]["email"]
        assert data["users"][0]["admin"] in [True, False]
        assert data["users"][0]["timestamp"]
        assert data["users"][0]["name"]
        assert data["users"][0]["group_name"]
        assert data["users"][0]["user_id"]


    def test_get_users_not_admin(self):

        response = self.client.get(
            "/api/users",
            headers=self.user_data["user1"]["auth_header"])


        assert(response.status_code == 403)


    def test_get_own_user_data_success(self):

        response = self.client.get(
            "/api/users/%s" % self.user_data["user1"]["user_id"],
            headers=self.user_data["user1"]["auth_header"])

        assert(response.status_code == 201)

        data = response.get_json()

        assert data["email"] == self.user_data["user1"]["email"]
        assert data["admin"] is False
        assert data["name"] == self.user_data["user1"]["name"]
        assert data["group_name"] == self.user_data["user1"]["group_name"]
        assert data["user_id"] == self.user_data["user1"]["user_id"]
        assert data["timestamp"]

    def test_get_user_data_as_admin_success(self):

        response = self.client.get(
            "/api/users/%s" % self.user_data["user1"]["user_id"],
            headers=self.user_data["admin"]["auth_header"])

        assert(response.status_code == 201)

        data = response.get_json()

        assert data["email"] == self.user_data["user1"]["email"]
        assert data["admin"] is self.user_data["user1"]["admin"]
        assert data["name"] == self.user_data["user1"]["name"]
        assert data["group_name"] == self.user_data["user1"]["group_name"]
        assert data["user_id"] == self.user_data["user1"]["user_id"]
        assert data["timestamp"]

    def test_get_mismatched_user_id_fail(self):
        response = self.client.get(
            "/api/users/%s" % self.user_data["user1"]["user_id"],
            headers=self.user_data["user2"]["auth_header"])

        assert(response.status_code == 403)


    def test_get_single_user_unrecognized(self):

        response = self.client.get(
            "/api/users/%s" % "unrecognized",
            headers=self.user_data["user1"]["auth_header"])

        assert(response.status_code == 404)

    def test_update_password_as_admin_success(self):
        response = self.client.put(
            "/api/users/%s" % self.user_data["user1"]["user_id"],
            headers=self.user_data["admin"]["auth_header"],
            json={"password":"new_password"})

        response_data = response.get_json()

        self.check_user_data_match(response_data, self.user_data["user1"])

        assert response.status_code == 200

        """
        Attempt to log in with the new password
        """

        auth_response = self.client.post("/api/auth_token",
            json= {"email": self.user_data["user1"]["email"],
                   "password": "new_password"})

        assert auth_response.status_code == 200

    def test_update_nonadmin_self_success(self):
        response = self.client.put(
            "/api/users/%s" % self.user_data["user1"]["user_id"],
            headers=self.user_data["user1"]["auth_header"],
            json={"group_name":"updated group name"})

        response_data = response.get_json()
        existing_user_data = copy.deepcopy(self.user_data["user1"])

        existing_user_data["group_name"] = "updated group name"

        self.check_user_data_match(response_data, existing_user_data)

        assert(response.status_code == 200)




    def test_update_user_id_mismatch_fail(self):
        response = self.client.put(
            "/api/users/%s" % self.user_data["user1"]["user_id"],
            headers=self.user_data["user2"]["auth_header"],
            json={"password":"new_password"})

        assert(response.status_code == 403)


    def test_update_unrecogized_fail(self):
        response = self.client.put(
            "/api/users/%s" % "unrecognized",
            headers=self.user_data["user1"]["auth_header"],
            json={"password":"new_password"})

        assert(response.status_code == 404)


    def test_update_no_matching_fields_fail(self):
        response = self.client.put(
            "/api/users/%s" % self.user_data["user1"]["user_id"],
            headers=self.user_data["user1"]["auth_header"],
            json={"random_field":"random_field_value"})

        assert(response.status_code == 400)


    def test_update_duplicated_email_fail(self):
        response = self.client.put(
            "/api/users/%s" % self.user_data["user1"]["user_id"],
            headers=self.user_data["user1"]["auth_header"],
            json={"email":self.user_data["user2"]["email"]})

        assert(response.status_code == 422)


    def test_update_set_self_admin_fail(self):

        response = self.client.put(
            "/api/users/%s" % self.user_data["user1"]["user_id"],
            headers=self.user_data["user1"]["auth_header"],
            json={"admin":True})

        assert(response.status_code == 403)
