from flask import g

import expungeservice
from expungeservice.database.db_util import rollback_errors
from expungeservice.stats import save_result
from tests.factories.crawler_factory import CrawlerFactory
from expungeservice.database import get_database
from tests.endpoints.endpoint_util import EndpointShared


class TestStats(EndpointShared):


    def test_save_result(self):


        user_id = self.user_data["user1"]["user_id"]

        with expungeservice.create_app("development").app_context():

            expungeservice.request.before() #Opens a db connection at g.database

            request_data = {
                "first_name":"John",
                "last_name":"Doe",
                "middle_name":"Test",
                "birth_date":"01/01/1980",
            }

            record = CrawlerFactory.create(CrawlerFactory.setup())

            save_result(user_id, request_data, record)

            g.database.connection.commit()

            self.check_search_result_saved(
                self.user_data["user1"]["user_id"], request_data,
                num_eligible_charges=6, num_charges=9)

