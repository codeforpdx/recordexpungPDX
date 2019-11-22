from flask import g
import hashlib

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

            search_param_string = (
                user_id +
                request_data["first_name"] +
                request_data["last_name"] +
                request_data["middle_name"] +
                request_data["birth_date"])

            hashed_search_params = hashlib.sha256(search_param_string.encode()).hexdigest()

            g.database.cursor.execute(
                    """
                    SELECT * FROM SEARCH_RESULTS
                    WHERE hashed_search_params  = %(hashed_search_params)s
                    ;
                    """,{'hashed_search_params': hashed_search_params})

            result = g.database.cursor.fetchone()._asdict()
            assert result["num_eligible_charges"] == 6
            assert result["num_charges"] == 9

            g.database.cursor.execute(
                    """
                    DELETE FROM SEARCH_RESULTS
                    WHERE hashed_search_params = %(hashed_search_params)s
                    ;
                    """,{'hashed_search_params': hashed_search_params})
            g.database.connection.commit()
