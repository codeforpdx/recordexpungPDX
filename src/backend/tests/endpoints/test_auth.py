import pytest
import os
import time
import datetime

from flask import jsonify, current_app

import expungeservice

@pytest.fixture(scope='module')
def app():
    return expungeservice.create_app('development')

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_hello(client):
    response = client.get('/hello')
    assert(response.data == b'Hello, world!')

email = 'test_user@test.com'
password = 'test_password'

def create_user(client, email, password):
    return client.post('api/v0.1/users', json={
        'email': email,
        'password': password,
    })

def get_auth_token(client, email, password):
    return client.get('/api/v0.1/auth_token', json={
        'email': email,
        'password': password,
    })

def test_create_user(client):
    response = create_user(client, email, password)
    assert(response.status_code == 201)

    data = response.get_json()
    assert(data['email'] == email)

def test_create_user_collision(client):
    response = create_user(client, email, password)
    assert(response.status_code == 202)

def test_auth_token_valid_credentials(client):
    response = get_auth_token(client, 'test_user@test.com', 'test_password')

    assert(response.status_code == 200)
    assert(response.headers.get('Content-type') == 'application/json')
    data = response.get_json()
    assert('auth_token' in data)
    assert(len(data['auth_token']))

def test_auth_token_invalid_username(client):
    response = get_auth_token(client, 'wrong_user@test.com', 'test_password')
    assert(response.status_code == 401)

def test_login_invalid_pasword(client):
    response = get_auth_token(client, 'test_user@test.com', 'wrong_password')
    assert(response.status_code == 401)

def test_access_valid_auth_token(client):
    response = get_auth_token(client, 'test_user@test.com', 'test_password')
    response = client.get('/api/v0.1/test/protected', headers={
        'Authorization': 'Bearer {}'.format(response.get_json()['auth_token'])
    })
    assert(response.status_code == 200)

def test_access_invalid_auth_token(client):
    response = get_auth_token(client, 'test_user@test.com', 'test_password')
    response = client.get('/api/v0.1/test/protected', headers={
        'Authorization': 'Bearer {}'.format('Invalid auth token')
    })
    assert(response.status_code == 401)

def test_access_expired_auth_token():
    app = expungeservice.create_app('development')
    app.config['JWT_EXPIRY_TIMER'] = datetime.timedelta(seconds=0)

    client = app.test_client()

    response = get_auth_token(client, 'test_user@test.com', 'test_password')
    time.sleep(1)
    response = client.get('/api/v0.1/test/protected', headers={
        'Authorization': 'Bearer {}'.format(response.get_json()['auth_token'])
    })
    assert(response.status_code == 401)
