import pytest
import os
import time
import datetime
import unittest

from flask import jsonify, current_app, g, request
from werkzeug.security import generate_password_hash

import expungeservice
from tests.endpoints.endpoint_util import EndpointShared


class TestUsers(EndpointShared):

    def test_get_users_success(self):

        response = self.client.get(
            "/api/users",
            headers=self.admin_auth_header)

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
            headers=self.user_auth_header
                )

        assert(response.status_code == 403)
