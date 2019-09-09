import unittest

from datetime import datetime
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe
from expungeservice.models.record import Record


class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = CrawlerFactory.setup()

    def test_search_function(self):
        record = CrawlerFactory.create(self.crawler, JohnDoe.RECORD, {'X0001': CaseDetails.CASE_X1,
                                                             'X0002': CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
                                                             'X0003': CaseDetails.CASE_WITHOUT_DISPOS})

        assert record.__class__ == Record
        assert len(record.cases) == 3

        assert len(record.cases[0].charges) == 3
        assert len(record.cases[1].charges) == 1
        assert len(record.cases[2].charges) == 3

        assert record.cases[0].charges[0].disposition.ruling == 'Convicted - Failure to Appear'
        assert record.cases[0].charges[0].disposition.date == datetime.date(datetime.strptime('06/12/2017', '%m/%d/%Y'))
        assert record.cases[0].charges[1].disposition.ruling == 'Dismissed'
        assert record.cases[0].charges[1].disposition.date == datetime.date(datetime.strptime('06/12/2017', '%m/%d/%Y'))
        assert record.cases[0].charges[2].disposition.ruling == 'Dismissed'
        assert record.cases[0].charges[2].disposition.date == datetime.date(datetime.strptime('06/12/2017', '%m/%d/%Y'))

        assert record.cases[1].charges[0].disposition.ruling == 'Dismissed'
        assert record.cases[1].charges[0].disposition.date == datetime.date(datetime.strptime('04/30/1992', '%m/%d/%Y'))

        assert record.cases[2].charges[0].disposition is None
        assert record.cases[2].charges[0].disposition is None
        assert record.cases[2].charges[1].disposition is None
        assert record.cases[2].charges[1].disposition is None
        assert record.cases[2].charges[2].disposition is None
        assert record.cases[2].charges[2].disposition is None

    def test_a_blank_search_response(self):
        record = CrawlerFactory.create(self.crawler, JohnDoe.BLANK_RECORD, {})

        assert len(record.cases) == 0

    def test_single_charge_conviction(self):
        record = CrawlerFactory.create(self.crawler, JohnDoe.SINGLE_CASE_RECORD, {'CASEJD1': CaseDetails.CASEJD1})

        assert len(record.cases) == 1
        assert len(record.cases[0].charges) == 1

        assert record.cases[0].charges[0].name == 'Loading Zone'
        assert record.cases[0].charges[0].statute == '29'
        assert record.cases[0].charges[0].level == 'Violation Unclassified'
        assert record.cases[0].charges[0].date == datetime.date(datetime.strptime('09/04/2008', '%m/%d/%Y'))
        assert record.cases[0].charges[0].disposition.ruling == 'Convicted'
        assert record.cases[0].charges[0].disposition.date == datetime.date(datetime.strptime('11/18/2008', '%m/%d/%Y'))

    def test_nonzero_balance_due_on_case(self):
        record = CrawlerFactory.create(self.crawler, JohnDoe.RECORD, {'X0001': CaseDetails.CASE_X1,
                                                             'X0002': CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
                                                             'X0003': CaseDetails.CASE_WITHOUT_DISPOS})

        assert record.cases[0].get_balance_due() == 1516.80

    def test_zero_balance_due_on_case(self):
        record = CrawlerFactory.create(self.crawler, JohnDoe.SINGLE_CASE_RECORD, {'CASEJD1': CaseDetails.CASEJD1})

        assert record.cases[0].get_balance_due() == 0
