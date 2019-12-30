import copy

import pytest
from werkzeug.security import generate_password_hash

from tests.endpoints.endpoint_util import EndpointShared


@pytest.fixture
def service():
    return EndpointShared()

@pytest.fixture(autouse=True)
def setup_and_teardown(service):
    service.setup()

    service.user_data["new_user"] = {
        "email": "pytest_create_user@endpoint_test.com",
        "password": "new_password",
        "hashed_password": generate_password_hash("new_password"),
        "name": "new name",
        "group_name": "new group name",
        "admin": False
    }
    yield
    service.teardown()

def check_user_data_match(created_user, reference_user):
    assert created_user["email"] == reference_user["email"]
    assert created_user["name"] == reference_user["name"]
    assert created_user["group_name"] == reference_user["group_name"]
    assert created_user["admin"] == reference_user["admin"]
    assert created_user["timestamp"]

def test_create_success(service):
    service.login(service.user_data["admin"]["email"], service.user_data["admin"]["password"])
    response = service.client.post(
        "/api/users",
        json=service.user_data["new_user"])

    assert(response.status_code == 201)

    data = response.get_json()
    check_user_data_match(data, service.user_data["new_user"])

def test_create_no_auth(service):
    response = service.client.post(
        "/api/users",
        headers={
            "Authorization": ""},
        json=service.user_data["new_user"])
    assert(response.status_code == 401)

def test_create_missing_data_field(service):
    service.login(service.user_data["admin"]["email"], service.user_data["admin"]["password"])

    response = service.client.post(
        "/api/users",
        json={"email": service.user_data["new_user"]["email"],
              "name": service.user_data["new_user"]["name"],
              "group_name": service.user_data["new_user"]["group_name"],
              # "password": new_password,
              "admin": True})

    assert(response.status_code == 400)

def test_create_duplicate_email(service):
    service.login(service.user_data["admin"]["email"], service.user_data["admin"]["password"])

    response = service.client.post(
        "/api/users",
        json=service.user_data["new_user"])

    assert(response.status_code == 201)

    response = service.client.post(
        "/api/users",
        json=service.user_data["new_user"])

    assert(response.status_code == 422)

def test_create_short_password(service):
    service.login(service.user_data["admin"]["email"], service.user_data["admin"]["password"])

    new_email = "pytest_create_user@endpoint_test.com"
    short_password = "shrt_pw"

    response = service.client.post(
        "/api/users",
        json={"email": service.user_data["new_user"]["email"],
              "name": service.user_data["new_user"]["name"],
              "group_name": service.user_data["new_user"]["group_name"],
              "password": short_password,
              "admin": False}
    )

    assert(response.status_code == 422)

def test_create_not_admin(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

    new_email = "pytest_create_user@endpoint_test.com"
    new_password = "new_password"

    response = service.client.post(
        "/api/users",
        json=service.user_data["new_user"])

    assert(response.status_code == 403)

def test_get_users_success(service):
    service.login(service.user_data["admin"]["email"], service.user_data["admin"]["password"])
    response = service.client.get("/api/users")

    assert(response.status_code == 201)

    data = response.get_json()

    assert data["users"][0]["email"]
    assert data["users"][0]["admin"] in [True, False]
    assert data["users"][0]["timestamp"]
    assert data["users"][0]["name"]
    assert data["users"][0]["group"]
    assert data["users"][0]["id"]

def test_get_users_not_admin(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    response = service.client.get("/api/users")
    assert(response.status_code == 403)

def test_get_own_user_data_success(service):
    def check_response_success(response, user_data):
        assert (response.status_code == 201)
        data = response.get_json()
        assert data["email"] == user_data["user1"]["email"]
        assert not data["admin"]
        assert data["name"] == user_data["user1"]["name"]
        assert data["group_name"] == user_data["user1"]["group_name"]
        assert data["user_id"] == user_data["user1"]["user_id"]
        assert data["timestamp"]

    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

    response = service.client.get("/api/users/%s" % service.user_data["user1"]["user_id"])
    check_response_success(response, service.user_data)

    response_without_explicit_id = service.client.get("/api/user")
    check_response_success(response_without_explicit_id, service.user_data)

def test_get_user_data_as_admin_success(service):
    service.login(service.user_data["admin"]["email"], service.user_data["admin"]["password"])
    response = service.client.get(
        "/api/users/%s" % service.user_data["user1"]["user_id"])

    assert(response.status_code == 201)

    data = response.get_json()

    assert data["email"] == service.user_data["user1"]["email"]
    assert data["admin"] is service.user_data["user1"]["admin"]
    assert data["name"] == service.user_data["user1"]["name"]
    assert data["group_name"] == service.user_data["user1"]["group_name"]
    assert data["user_id"] == service.user_data["user1"]["user_id"]
    assert data["timestamp"]

def test_get_mismatched_user_id_fail(service):
    service.login(service.user_data["user2"]["email"], service.user_data["user2"]["password"])
    response = service.client.get("/api/users/%s" % service.user_data["user1"]["user_id"])

    assert(response.status_code == 403)

def test_get_single_user_unrecognized(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    response = service.client.get("/api/users/%s" % "unrecognized")

    assert(response.status_code == 404)

def test_update_password_as_admin_success(service):
    service.login(service.user_data["admin"]["email"], service.user_data["admin"]["password"])
    response = service.client.put(
        "/api/users/%s" % service.user_data["user1"]["user_id"],
        json={"password":"new_password"})

    response_data = response.get_json()

    check_user_data_match(response_data, service.user_data["user1"])

    assert response.status_code == 200

    """
    Attempt to log in with the new password
    """

    auth_response = service.client.post("/api/auth_token",
        json= {"email": service.user_data["user1"]["email"],
               "password": "new_password"})

    assert auth_response.status_code == 200

def test_update_nonadmin_self_success(service):
    def check_response_success(response, user_data, check_user_data_match_fn):
        response_data = response.get_json()
        existing_user_data = copy.deepcopy(user_data["user1"])
        existing_user_data["group_name"] = "updated group name"
        check_user_data_match_fn(response_data, existing_user_data)
        assert (response.status_code == 200)

    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    response = service.client.put(
        "/api/users/%s" % service.user_data["user1"]["user_id"],
        json={"group_name":"updated group name"})
    check_response_success(response, service.user_data, check_user_data_match)

    response_without_explicit_id = service.client.put(
        "/api/user",
        json={"group_name":"updated group name"})
    check_response_success(response_without_explicit_id, service.user_data, check_user_data_match)

def test_update_user_id_mismatch_fail(service):
    service.login(service.user_data["user2"]["email"], service.user_data["user2"]["password"])
    response = service.client.put(
        "/api/users/%s" % service.user_data["user1"]["user_id"],
        json={"password":"new_password"})

    assert(response.status_code == 403)

def test_update_unrecogized_fail(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    response = service.client.put(
        "/api/users/%s" % "unrecognized",
        json={"password":"new_password"})
    assert(response.status_code == 404)

    response_without_explicit_id = service.client.put(
        "/api/user/",
        json={"password":"new_password"})
    assert(response_without_explicit_id.status_code == 404)

def test_update_no_matching_fields_fail(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    response = service.client.put(
        "/api/users/%s" % service.user_data["user1"]["user_id"],
        json={"random_field":"random_field_value"})
    assert(response.status_code == 400)

    response_without_explicit_id = service.client.put(
        "/api/user",
        json={"random_field":"random_field_value"})
    assert(response_without_explicit_id.status_code == 400)

def test_update_duplicated_email_fail(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    response = service.client.put(
        "/api/users/%s" % service.user_data["user1"]["user_id"],
        json={"email":service.user_data["user2"]["email"]})
    assert(response.status_code == 422)

    response_without_explicit_id = service.client.put(
        "/api/user",
        json={"email": service.user_data["user2"]["email"]})
    assert (response_without_explicit_id.status_code == 422)

def test_update_set_self_admin_fail(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    response = service.client.put(
        "/api/users/%s" % service.user_data["user1"]["user_id"],
        json={"admin":True})
    assert(response.status_code == 403)

    response_without_explicit_id = service.client.put(
        "/api/user",
        json={"admin":True})
    assert(response_without_explicit_id.status_code == 403)
