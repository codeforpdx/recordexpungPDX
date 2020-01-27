import pytest
from flask import g

from expungeservice import stats
from tests.endpoints.endpoint_util import EndpointShared
from tests.factories.crawler_factory import CrawlerFactory
from expungeservice.database import get_database


@pytest.fixture
def service():
    return EndpointShared()


@pytest.fixture(autouse=True)
def setup_and_teardown(service):
    service.setup()
    yield
    service.teardown()


def test_save_result(service):
    with service.client:
        request_data = {
            "first_name": "John",
            "last_name": "Doe",
            "middle_name": "Test",
            "birth_date": "01/01/1980",
        }

        record = CrawlerFactory.create(CrawlerFactory.setup())

        service.login(service.user_data["user1"]["email"], service.user_data["user1"]["password"])

        g.database = get_database()

        stats.save_result(request_data, record)

        g.database.connection.commit()

    service.check_search_result_saved(
        service.user_data["user1"]["user_id"], request_data, num_eligible_charges=6, num_charges=9
    )
