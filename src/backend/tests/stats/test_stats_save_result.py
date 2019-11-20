from flask import g

import expungeservice
from expungeservice.database.db_util import rollback_errors
from expungeservice.stats import save_result
from tests.factories.crawler_factory import CrawlerFactory
from expungeservice.database import get_database
from tests.endpoints.endpoint_util import EndpointShared


class TestStats():

    def test_save_result(self):

        with expungeservice.create_app("development").app_context():

            expungeservice.request.before()
            database = get_database()
            user_id = "user_id"
            request_data = {
                "first_name":"first_name",
                "last_name":"last_name",
                "middle_name":"middle_name",
                "birth_date":"birth_date",
            }


            record = CrawlerFactory.create(CrawlerFactory.setup())

            save_result(user_id, request_data, record)

            expungeservice.request.after(None)

            hashed_search_params = hash(
                user_id +
                "first_name" +
                "last_name" +
                "middle_name" +
                "birth_date")
            database.cursor.execute(
                    """
                    SELECT * FROM SEARCH_RESULTS
                    WHERE cast(hashed_search_params as bigint) = %(hashed_search_params)s
                    ;
                    """,{'hashed_search_params': hashed_search_params})

            result = database.cursor.fetchone()._asdict()
            assert result["num_eligible_charges"] == 6
            assert result["num_charges"] == 9

            database.cursor.execute(
                    """
                    DELETE FROM SEARCH_RESULTS
                    WHERE cast(hashed_search_params as bigint) = %(hashed_search_params)s
                    ;
                    """,{'hashed_search_params': hashed_search_params})
            database.connection.commit()