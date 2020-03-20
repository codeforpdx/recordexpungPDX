from itertools import product

import requests_mock

from expungeservice.crawler.crawler import Crawler
from expungeservice.crawler.request import URL
from expungeservice.models.record import Record
from tests.fixtures.post_login_page import PostLoginPage
from tests.fixtures.search_page_response import SearchPageResponse
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe


class CrawlerFactory:
    @staticmethod
    def create(
        record=JohnDoe.RECORD_WITH_CLOSED_CASES,
        cases={"X0001": CaseDetails.case_x(), "X0002": CaseDetails.case_x(), "X0003": CaseDetails.case_x()},
    ):
        base_url = "https://publicaccess.courts.oregon.gov/PublicAccessLogin/"
        crawler = Crawler()
        with requests_mock.Mocker() as m:
            m.post(URL.login_url(), text=PostLoginPage.POST_LOGIN_PAGE)
            crawler.login("username", "password")

            m.post(
                "{}{}".format(base_url, "Search.aspx?ID=100"), [{"text": SearchPageResponse.RESPONSE}, {"text": record}]
            )

            for key, value in cases.items():
                m.get("{}{}{}".format(base_url, "CaseDetail.aspx?CaseID=", key), text=value)

            ambiguous_cases = crawler.search("John", "Doe")
            cases_list = [list(cases) for cases in product(*ambiguous_cases)]
            ambiguous_record = [Record(cases) for cases in cases_list]
            return ambiguous_record[0]  # TODO: We currently pretend we cannot get an ambiguous record/case/charge
