import unittest

from datetime import date as date_class
from dateutil.relativedelta import relativedelta
from expungeservice.expunger.expunger import Expunger
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe


class TestCrawlerAndExpunger(unittest.TestCase):

    ONE_YEAR_AGO = (date_class.today() + relativedelta(years=-1))
    TWO_YEARS_AGO = (date_class.today() + relativedelta(years=-2))
    FIFTEEN_YEARS_AGO = (date_class.today() + relativedelta(years=-15))

    def setUp(self):
        self.crawler = CrawlerFactory.setup()

    def test_expunger_with_open_case(self):
        record = CrawlerFactory.create(self.crawler, JohnDoe.RECORD, {'X0001': CaseDetails.CASE_X1,
                                                             'X0002': CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
                                                             'X0003': CaseDetails.CASE_WITHOUT_DISPOS})
        expunger = Expunger(record)
        assert expunger.run() is False
        assert expunger.errors == ['Open cases exist']

    def test_expunger_with_an_empty_record(self):
        record = CrawlerFactory.create(self.crawler, JohnDoe.BLANK_RECORD, {})
        expunger = Expunger(record)

        assert expunger.run() is True
        assert expunger.most_recent_dismissal is None
        assert expunger.most_recent_conviction is None

    def test_partial_dispos(self):
        crawler = CrawlerFactory.setup()
        record = CrawlerFactory.create(crawler, JohnDoe.SINGLE_CASE_RECORD, {'CASEJD1': CaseDetails.CASE_WITH_PARTIAL_DISPOS})

        expunger = Expunger(record)
        expunger.run()

    def test_case_without_dispos(self):
        crawler = CrawlerFactory.setup()
        record = CrawlerFactory.create(crawler, JohnDoe.SINGLE_CASE_RECORD, {'CASEJD1': CaseDetails.CASE_WITHOUT_DISPOS})

        expunger = Expunger(record)
        expunger.run()

    def test_expunger_categorizes_charges(self):
        record = CrawlerFactory.create(self.crawler,
                              cases={'X0001': CaseDetails.case_x(dispo_ruling_1='Convicted - Failure to show',
                                                                 dispo_ruling_2='Dismissed',
                                                                 dispo_ruling_3='Acquitted'),
                                     'X0002': CaseDetails.case_x(dispo_ruling_1='Dismissed',
                                                                 dispo_ruling_2='Convicted',
                                                                 dispo_ruling_3='Convicted'),
                                     'X0003': CaseDetails.case_x(dispo_ruling_1='No Complaint',
                                                                 dispo_ruling_2='Dismissed',
                                                                 dispo_ruling_3='Convicted')})
        expunger = Expunger(record)

        assert expunger.run() is True
        assert len(expunger.acquittals) == 5
        assert len(expunger.convictions) == 4

    def test_expunger_runs_time_analyzer(self):
        record = CrawlerFactory.create(self.crawler,
                              cases={'X0001': CaseDetails.case_x(arrest_date=self.FIFTEEN_YEARS_AGO.strftime('%m/%d/%Y'),
                                                                 dispo_date=self.FIFTEEN_YEARS_AGO.strftime('%m/%d/%Y'),
                                                                 dispo_ruling_1='Dismissed',
                                                                 dispo_ruling_2='Convicted',
                                                                 dispo_ruling_3='Acquitted'),
                                     'X0002': CaseDetails.case_x(arrest_date=self.TWO_YEARS_AGO.strftime('%m/%d/%Y'),
                                                                 dispo_ruling_1='Dismissed',
                                                                 dispo_ruling_2='Dismissed',
                                                                 dispo_ruling_3='Dismissed'),
                                     'X0003': CaseDetails.case_x(arrest_date=self.ONE_YEAR_AGO.strftime('%m/%d/%Y'),
                                                                 dispo_ruling_1='No Complaint',
                                                                 dispo_ruling_2='No Complaint',
                                                                 dispo_ruling_3='No Complaint')})
        expunger = Expunger(record)

        assert expunger.run() is True

        assert expunger.most_recent_conviction is None
        assert expunger.second_most_recent_conviction is None
        assert expunger.most_recent_dismissal.disposition.ruling == 'No Complaint'
        assert len(expunger.acquittals) == 8

        assert record.cases[0].charges[0].expungement_result.time_eligibility.status is False
        assert record.cases[0].charges[1].expungement_result.time_eligibility.status is True
        assert record.cases[0].charges[2].expungement_result.time_eligibility.status is False

        assert record.cases[1].charges[0].expungement_result.time_eligibility.status is False
        assert record.cases[1].charges[1].expungement_result.time_eligibility.status is False
        assert record.cases[1].charges[2].expungement_result.time_eligibility.status is False

        assert record.cases[2].charges[0].expungement_result.time_eligibility.status is True
        assert record.cases[2].charges[1].expungement_result.time_eligibility.status is True
        assert record.cases[2].charges[2].expungement_result.time_eligibility.status is True
