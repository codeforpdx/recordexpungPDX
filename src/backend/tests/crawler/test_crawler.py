import unittest
import requests_mock

from tests.fixtures.post_login_page import PostLoginPage
from tests.fixtures.search_page_response import SearchPageResponse
from tests.fixtures.john_doe import JohnDoe
from tests.fixtures.case_details import CaseDetails

from expungeservice.crawler.crawler import Crawler
from expungeservice.crawler.request import URL


class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()
        with requests_mock.Mocker() as m:
            m.post(URL.login_url(), text=PostLoginPage.POST_LOGIN_PAGE)
            self.crawler.login('username', 'password')

    def test_search_function(self):
        base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'
        with requests_mock.Mocker() as m:
            m.post(base_url + 'Search.aspx?ID=100', [{'text': SearchPageResponse.RESPONSE}, {'text': JohnDoe.RECORD}])

            base_url += 'CaseDetail.aspx'
            m.get(base_url + '?CaseID=X0001', text=CaseDetails.CASE_X1)
            m.get(base_url + '?CaseID=X0002', text=CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION)
            m.get(base_url + '?CaseID=X0003', text=CaseDetails.CASE_WITHOUT_DISPOS)

            self.crawler.search('John', 'Doe')

        assert len(self.crawler.result.cases) == 3

        assert len(self.crawler.result.cases[0].charges) == 3
        assert len(self.crawler.result.cases[1].charges) == 1
        assert len(self.crawler.result.cases[2].charges) == 3

        assert self.crawler.result.cases[0].charges[0].disposition.ruling == 'Convicted - Failure to Appear'
        assert self.crawler.result.cases[0].charges[0].disposition.date == '06/12/2017'
        assert self.crawler.result.cases[0].charges[1].disposition.ruling == 'Dismissed'
        assert self.crawler.result.cases[0].charges[1].disposition.date == '06/12/2017'
        assert self.crawler.result.cases[0].charges[2].disposition.ruling == 'Hmmmm'
        assert self.crawler.result.cases[0].charges[2].disposition.date == '06/12/2017'

        assert self.crawler.result.cases[1].charges[0].disposition.ruling == 'Dismissed'
        assert self.crawler.result.cases[1].charges[0].disposition.date == '04/30/1992'

        assert self.crawler.result.cases[2].charges[0].disposition.ruling is None
        assert self.crawler.result.cases[2].charges[0].disposition.date is None
        assert self.crawler.result.cases[2].charges[1].disposition.ruling is None
        assert self.crawler.result.cases[2].charges[1].disposition.date is None
        assert self.crawler.result.cases[2].charges[2].disposition.ruling is None
        assert self.crawler.result.cases[2].charges[2].disposition.date is None

    def test_a_blank_search_response(self):
        base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'
        with requests_mock.Mocker() as m:
            m.post(base_url + 'Search.aspx?ID=100', [{'text': SearchPageResponse.RESPONSE},
                                                     {'text': JohnDoe.BLANK_RECORD}])
            self.crawler.search('John', 'Doe')

        assert len(self.crawler.result.cases) == 0

    def test_single_charge_conviction(self):
        base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'
        with requests_mock.Mocker() as m:
            m.post(base_url + 'Search.aspx?ID=100', [{'text': SearchPageResponse.RESPONSE},
                                                     {'text': JohnDoe.SINGLE_CASE_RECORD}])
            base_url += 'CaseDetail.aspx'
            m.get(base_url + '?CaseID=CASEJD1', text=CaseDetails.CASEJD1)

            self.crawler.search('John', 'Doe')

        assert len(self.crawler.result.cases) == 1
        assert len(self.crawler.result.cases[0].charges) == 1

        assert self.crawler.result.cases[0].charges[0].name == 'Loading Zone'
        assert self.crawler.result.cases[0].charges[0].statute == '29'
        assert self.crawler.result.cases[0].charges[0].level == 'Violation Unclassified'
        assert self.crawler.result.cases[0].charges[0].date == '09/04/2008'
        assert self.crawler.result.cases[0].charges[0].disposition.ruling == 'Convicted'
        assert self.crawler.result.cases[0].charges[0].disposition.date == '11/18/2008'
