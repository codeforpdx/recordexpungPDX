import json

import pytest

from expungeservice.endpoints import search
from tests.endpoints.endpoint_util import EndpointShared
from tests.factories.crawler_factory import CrawlerFactory
from expungeservice.serializer import ExpungeModelEncoder


@pytest.fixture
def service():
    return EndpointShared()


@pytest.fixture(autouse=True)
def setup_and_teardown(service):
    service.setup()

    service.crawler = CrawlerFactory.setup()
    service.crawler.logged_in = True
    service.mock_record = {"john_doe": CrawlerFactory.create(service.crawler)}
    service.search_request_data = {
        "first_name": "John",
        "last_name": "Doe",
        "middle_name": "",
        "birth_date": "02/02/1990",
    }
    yield
    service.teardown()


def mock_login(return_value):
    return lambda s, username, password, close_session=False: return_value


def mock_search(service, mocked_record_name):
    return lambda s, first_name, last_name, middle_name, birth_date: service.mock_record[mocked_record_name]


def mock_save_result_fail(user_id, request_data, record):
    raise Exception("Exception to test failing save_result")


def test_search(service, monkeypatch):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

    monkeypatch.setattr(search.Crawler, "login", mock_login(True))
    monkeypatch.setattr(search.Crawler, "search", mock_search(service, "john_doe"))

    """
    A separate test, below, verifies that the save-result step
    also works. Here, we mock the function to reduce the scope of the test.
    """
    monkeypatch.setattr(search, "save_result", lambda user_id, request_data, record: None)

    """
    as a more unit-y unit test, we could make the encrypted cookie
    ""manually" in the test code ...
    But attaching a cookie client-side isn't really a thing. So, use the oeci endpoint.
    """

    service.client.post(
        "/api/oeci_login", json={"oeci_username": "correctusername", "oeci_password": "correctpassword"}
    )

    assert service.client.cookie_jar._cookies["localhost.local"]["/"]["oeci_token"]

    response = service.client.post("/api/search", json=service.search_request_data)

    assert response.status_code == 200
    data = response.get_json()["data"]

    """
    Check that the resulting "record" field in the response matches what we gave to the
    mock search function.
    (use this json encode-decode approach because it turns a Record into a dict.)
    """
    assert data["record"] == json.loads(json.dumps(service.mock_record["john_doe"], cls=ExpungeModelEncoder))


def test_search_fails_without_oeci_token(service):
    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

    response = service.client.post("/api/search", json=service.search_request_data)

    assert response.status_code == 401


def test_search_creates_save_results(service, monkeypatch):
    """
    This is the same test as above except it includes the save-results step. Less unit-y,
    more of a vertical test.
    """

    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

    monkeypatch.setattr(search.Crawler, "login", mock_login(True))
    monkeypatch.setattr(search.Crawler, "search", mock_search(service, "john_doe"))

    service.client.post(
        "/api/oeci_login", json={"oeci_username": "correctusername", "oeci_password": "correctpassword"}
    )

    assert service.client.cookie_jar._cookies["localhost.local"]["/"]["oeci_token"]

    response = service.client.post("/api/search", json=service.search_request_data)

    assert response.status_code == 200
    data = response.get_json()["data"]

    """
    Check that the resulting "record" field in the response matches
    what we gave to the mock search function.

    (use this json encode-decode approach because it turns a Record into a dict.)
    """
    assert data["record"] == json.loads(json.dumps(service.mock_record["john_doe"], cls=ExpungeModelEncoder))

    service.check_search_result_saved(
        service.user_data["user1"]["user_id"], service.search_request_data, num_eligible_charges=6, num_charges=9
    )


def test_search_with_failing_save_results(service, monkeypatch):
    """
    The search endpoint should succeed even if something goes wrong with the save-result step.

    """

    service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])
    monkeypatch.setattr(search.Crawler, "login", mock_login(True))
    monkeypatch.setattr(search.Crawler, "search", mock_search(service, "john_doe"))
    monkeypatch.setattr(search, "save_result", mock_save_result_fail)

    service.client.post(
        "/api/oeci_login", json={"oeci_username": "correctusername", "oeci_password": "correctpassword"}
    )

    assert service.client.cookie_jar._cookies["localhost.local"]["/"]["oeci_token"]

    response = service.client.post("/api/search", json=service.search_request_data)

    assert response.status_code == 200
    data = response.get_json()["data"]

    """
    Check that the resulting "record" field in the response matches what we gave to the
    mock search function.
    (use this json encode-decode approach because it turns a Record into a dict.)
    """
    assert data["record"] == json.loads(json.dumps(service.mock_record["john_doe"], cls=ExpungeModelEncoder))
