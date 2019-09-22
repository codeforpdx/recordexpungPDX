import pytest
import os
import datetime
import unittest
from werkzeug.security import generate_password_hash
from flask import jsonify, current_app, g, request

from expungeservice.crawler.request import URL
from tests.fixtures.post_login_page import PostLoginPage

from expungeservice.database import user
import expungeservice

from expungeservice.endpoints import oeci_login


class TestOeciLogin(unittest.TestCase):

    def test_oeci_login_success(self):

        pass

    def test_oeci_login_invalid_credentials(self):

        pass
