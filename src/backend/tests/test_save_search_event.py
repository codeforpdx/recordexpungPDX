import pytest
from flask import g

from tests.endpoints.endpoint_util import EndpointShared
from tests.factories.crawler_factory import CrawlerFactory
from expungeservice.database import get_database
from expungeservice.database.db_util import save_search_event

@pytest.fixture
def service():
    return EndpointShared()


@pytest.fixture(autouse=True)
def setup_and_teardown(service):
    service.setup()
    yield
    service.teardown()


def test_save_search_event(service):
    with service.client:
        request_data = {
            "aliases": [{"first_name": "John", "last_name": "Doe", "middle_name": "Test", "birth_date": "01/01/1980",}]
        }

        record = CrawlerFactory.create()

        service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

        g.database = get_database()

        save_search_event(request_data, record)

        g.database.connection.commit()

    service.check_search_event_saved(
        service.user_data["user1"]["user_id"], request_data
    )
