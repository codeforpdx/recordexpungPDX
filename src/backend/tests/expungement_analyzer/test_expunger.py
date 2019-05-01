import unittest

from datetime import datetime
from expungeservice.expungement_analyzer.expunger import Expunger
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe


class TestExpungementAnalyzer(unittest.TestCase):

    def setUp(self):
        self.crawler = CrawlerFactory.setup()

    def test_expunger_with_open_case(self):
        CrawlerFactory.create(self.crawler, JohnDoe.RECORD, {'X0001': CaseDetails.CASE_X1,
                                                             'X0002': CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
                                                             'X0003': CaseDetails.CASE_WITHOUT_DISPOS})
        expunger = Expunger(self.crawler.result.cases)
        assert expunger.run() is False
        assert expunger.errors == ['Open cases exist']

    def test_expunger_with_an_empty_record(self):
        CrawlerFactory.create(self.crawler, JohnDoe.BLANK_RECORD, {})
        expunger = Expunger(self.crawler.result.cases)

        assert expunger.run() is True
        assert expunger._most_recent_acquittal is None
        assert expunger._most_recent_conviction is None

    def test_expunger(self):
        CrawlerFactory.create(self.crawler, JohnDoe.RECORD_WITH_CLOSED_CASES,
                              {'X0001': CaseDetails.CASE_X1,
                               'X0002': CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
                               'X0003': CaseDetails.CASE_X3})
        expunger = Expunger(self.crawler.result.cases)

        charge1, charge2, charge3 = self.crawler.result.cases[0].charges
        charge4 = self.crawler.result.cases[1].charges[0]
        charge5, charge6, charge7 = self.crawler.result.cases[2].charges

        assert expunger.run() is True
        assert expunger._most_recent_acquittal.date == datetime.date(datetime.strptime('03/12/2017', '%m/%d/%Y'))
        assert expunger._most_recent_conviction is None

        assert charge1.expungement_result.type_eligibility is True
        assert charge2.expungement_result.type_eligibility is True
        assert charge3.expungement_result.type_eligibility is True

        assert charge4.expungement_result.type_eligibility is True

        assert charge5.expungement_result.type_eligibility is True
        assert charge6.expungement_result.type_eligibility is True
        assert charge7.expungement_result.type_eligibility is True
