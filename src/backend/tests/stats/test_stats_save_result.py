import pytest
from flask import g, request


import expungeservice
from tests.factories.crawler_factory import CrawlerFactory
from tests.endpoints.endpoint_util import EndpointShared
from expungeservice.database import get_database


class TestStats(EndpointShared):
    @pytest.fixture(autouse=True)
    def setUp(self):
        EndpointShared.setUp(self)
        yield
        EndpointShared.tearDown(self)

    def test_save_result(self):

        with self.client:
            user_id = self.user_data["user1"]["user_id"]

            request_data = {
                "first_name":"John",
                "last_name":"Doe",
                "middle_name":"Test",
                "birth_date":"01/01/1980",
            }

            record = CrawlerFactory.create(CrawlerFactory.setup())

            self.login(self.user_data["user1"]["email"], self.user_data["user1"]["password"])

            g.database = get_database()

            expungeservice.stats.save_result(request_data, record)

            g.database.connection.commit()

        self.check_search_result_saved(
                self.user_data["user1"]["user_id"], request_data,
                num_eligible_charges=6, num_charges=9)
