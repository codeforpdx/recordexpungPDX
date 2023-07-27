import json
from typing import List, Any, Callable

import pytest

from expungeservice.crawler.crawler import Crawler
from expungeservice.models.case import Case
from tests.endpoints.endpoint_util import EndpointShared
from tests.factories.crawler_factory import CrawlerFactory
from expungeservice.record_creator import RecordCreator
from expungeservice.models.record import Alias
from expungeservice.endpoints.search import Search
from expungeservice.util import DateWithFuture as date


@pytest.fixture
def service():
    return EndpointShared()


@pytest.fixture(autouse=True)
def setup_and_teardown(service):
    service.mock_record = {"john_doe": CrawlerFactory.create()}
    service.search_request_data = {
        "aliases": [{"first_name": "John", "last_name": "Doe", "middle_name": "", "birth_date": "02/02/1990"}]
    }
    yield


def mock_login(return_value):
    return lambda s, username, password, close_session=False: return_value


def mock_search(service, mocked_record_name) -> Callable[[Any, Any, Any, Any, Any, Any], List[Case]]:
    def compute_cases(s, login_response, first_name, last_name, middle_name, birth_date):
        record = service.mock_record[mocked_record_name]
        return record.cases

    return compute_cases


def mock_search_fail() -> Callable[[Any, Any, Any, Any, Any, Any], List[Case]]:
    def throw_error(s, login_response, first_name, last_name, middle_name, birth_date):
        raise Exception()

    return throw_error


def check_response_record_matches_mock_crawler_search(record_dict, mock_record):
    # response data is now sorted by date just before return in search.py
    # so test cases should be sorted with same method when testing against search.py
    sorted_mock_record = RecordCreator.sort_record_by_case_date(mock_record)
    assert record_dict["total_balance_due"] == mock_record.total_balance_due
    case_numbers = [case["case_number"] for case in record_dict["cases"]]
    mocked_case_numbers = [case.summary.case_number for case in sorted_mock_record.cases]
    assert case_numbers == mocked_case_numbers


def test_search(service, monkeypatch):
    monkeypatch.setattr(Crawler, "attempt_login", mock_login("Successful login response"))
    monkeypatch.setattr(Crawler, "search", mock_search(service, "john_doe"))
    """
    as a more unit-y unit test, we could make the encrypted cookie
    ""manually" in the test code ...
    But attaching a cookie client-side isn't really a thing. So, use the oeci endpoint.
    """
    service.client.post(
        "/api/oeci_login", json={"oeci_username": "correctusername", "oeci_password": "correctpassword"}
    )

    assert any(cookie.key == "oeci_token" for cookie in service.client.cookie_jar)

    response = service.client.post("/api/search", json=service.search_request_data)
    assert response.status_code == 200
    data = json.loads(response.data)

    check_response_record_matches_mock_crawler_search(data["record"], service.mock_record["john_doe"])


def test_search_fails_without_oeci_token(service):
    response = service.client.post("/api/search", json=service.search_request_data)
    assert response.status_code == 401


def test_search_creates_save_search_event(service, monkeypatch):
    """
    This is the same test as above except it includes the save-results step. Less unit-y,
    more of a vertical test.
    """
    monkeypatch.setattr(Crawler, "attempt_login", mock_login("Successful login response"))
    monkeypatch.setattr(Crawler, "search", mock_search(service, "john_doe"))
    service.client.post(
        "/api/oeci_login", json={"oeci_username": "correctusername", "oeci_password": "correctpassword"}
    )
    assert any(cookie.key == "oeci_token" for cookie in service.client.cookie_jar)

    response = service.client.post("/api/search", json=service.search_request_data)

    assert response.status_code == 200
    data = json.loads(response.data)

    check_response_record_matches_mock_crawler_search(data["record"], service.mock_record["john_doe"])


def test_search_with_failing_save_event(service, monkeypatch):
    """
    The search endpoint should succeed even if something goes wrong with the save-result step.
    """
    monkeypatch.setattr(Crawler, "attempt_login", mock_login("Successful login response"))
    monkeypatch.setattr(Crawler, "search", mock_search(service, "john_doe"))
    service.client.post(
        "/api/oeci_login", json={"oeci_username": "correctusername", "oeci_password": "correctpassword"}
    )
    assert any(cookie.key == "oeci_token" for cookie in service.client.cookie_jar)

    response = service.client.post("/api/search", json=service.search_request_data)

    assert response.status_code == 200
    data = json.loads(response.data)

    check_response_record_matches_mock_crawler_search(data["record"], service.mock_record["john_doe"])


def test_search_cache(service, monkeypatch):

    monkeypatch.setattr(Crawler, "attempt_login", mock_login("Successful login response"))
    monkeypatch.setattr(Crawler, "search", mock_search(service, "john_doe"))

    test_alias = (Alias("john", "deer", "", ""),)
    test_alias_dictionary = [
        {"first_name": "john", "last_name": "deer", "middle_name": "", "birth_date": ""},
    ]

    Search._build_record_summary("username", "password", test_alias_dictionary, {}, {}, date.today())
    assert Search.search_cache[test_alias]


def test_search_cache_error(service, monkeypatch):

    monkeypatch.setattr(Crawler, "attempt_login", mock_login("Successful login response"))
    monkeypatch.setattr(Crawler, "search", mock_search_fail())
    test_fail_alias = (Alias("jane", "doe", "q", "June 29th"),)

    test_fail_alias_dictionary = [
        {"first_name": "jane", "last_name": "doe", "middle_name": "q", "birth_date": "June 29th"},
    ]

    Search._build_record_summary("username", "password", test_fail_alias_dictionary, {}, {}, date.today())

    assert not Search.search_cache[test_fail_alias]
