import base64
import cryptography
import json
from flask import current_app

from tests.endpoints.endpoint_util import EndpointShared
from expungeservice.crypto import DataCipher
import requests


class TestMockedOeci(EndpointShared):

    def setUp(self):
        EndpointShared.setUp(self)
        with self.app.app_context():

            self.cipher = DataCipher(
                key=current_app.config.get("JWT_SECRET_KEY"))


    def test_oeci_login_success(self):

        self.session = requests.Session()

        response = self.session.post("http://localhost/api/oeci_login", data={"oeci_username": "username",
                  "oeci_password": "password"})

        raise Exception("oeci endpoint mocker test case not implemented")


