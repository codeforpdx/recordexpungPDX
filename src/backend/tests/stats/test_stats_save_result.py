import pytest
from flask import g, request

from expungeservice.stats import stats
from tests.endpoints.endpoint_util import EndpointShared
from tests.factories.crawler_factory import CrawlerFactory
from expungeservice.database import get_database


class TestStats:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = EndpointShared()
        self.service.setup()
        yield
        self.service.teardown()

    def test_save_result(self):
        with self.service.client:
            request_data = {
                "first_name":"John",
                "last_name":"Doe",
                "middle_name":"Test",
                "birth_date":"01/01/1980",
            }

            record = CrawlerFactory.create(CrawlerFactory.setup())

            self.service.login(self.service.user_data["user1"]["email"], self.service.user_data["user1"]["password"])

            g.database = get_database()

            stats.save_result(request_data, record)

            g.database.connection.commit()

        self.service.check_search_result_saved(
                self.service.user_data["user1"]["user_id"], request_data,
                num_eligible_charges=6, num_charges=9)
