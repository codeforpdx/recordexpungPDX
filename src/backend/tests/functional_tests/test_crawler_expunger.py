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
        CrawlerFactory.create(self.crawler, JohnDoe.RECORD, {'X0001': CaseDetails.CASE_X1,
                                                             'X0002': CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
                                                             'X0003': CaseDetails.CASE_WITHOUT_DISPOS})
        expunger = Expunger(self.crawler.result.cases)
        assert expunger.run() is False
        assert expunger.errors == ['Open cases exist']

    def test_type_analyzer_runs_when_open_cases_exit(self):
        CrawlerFactory.create(self.crawler, JohnDoe.RECORD, {'X0001': CaseDetails.CASE_X1,
                                                             'X0002': CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
                                                             'X0003': CaseDetails.CASE_WITHOUT_DISPOS})
        expunger = Expunger(self.crawler.result.cases)
        expunger.run()

        assert expunger.cases[0].charges[1].expungement_result.type_eligibility is True

    def test_expunger_with_an_empty_record(self):
        CrawlerFactory.create(self.crawler, JohnDoe.BLANK_RECORD, {})
        expunger = Expunger(self.crawler.result.cases)

        assert expunger.run() is True
        assert expunger._most_recent_dismissal is None
        assert expunger._most_recent_conviction is None

    def test_expunger_categorizes_charges(self):
        CrawlerFactory.create(self.crawler,
                              cases={'X0001': CaseDetails.case_x(dispo_ruling_1='Convicted - Failure to show',
                                                                 dispo_ruling_2='Dismissed',
                                                                 dispo_ruling_3='Acquitted'),
                                     'X0002': CaseDetails.case_x(dispo_ruling_1='Dismissed',
                                                                 dispo_ruling_2='Convicted',
                                                                 dispo_ruling_3='Convicted'),
                                     'X0003': CaseDetails.case_x(dispo_ruling_1='No Complaint',
                                                                 dispo_ruling_2='Dismissed',
                                                                 dispo_ruling_3='Convicted')})
        expunger = Expunger(self.crawler.result.cases)

        assert expunger.run() is True
        assert len(expunger._acquittals) == 5
        assert len(expunger._convictions) == 4

    def test_expunger_calls_time_analyzer(self):
        CrawlerFactory.create(self.crawler,
                              cases={'X0001': CaseDetails.case_x(arrest_date=self.FIFTEEN_YEARS_AGO.strftime('%m/%d/%Y'),
                                                                 dispo_ruling_1='Dismissed',
                                                                 dispo_ruling_2='Dismissed',
                                                                 dispo_ruling_3='Acquitted'),
                                     'X0002': CaseDetails.case_x(arrest_date=self.TWO_YEARS_AGO.strftime('%m/%d/%Y'),
                                                                 dispo_ruling_1='Dismissed',
                                                                 dispo_ruling_2='Convicted',
                                                                 dispo_ruling_3='Dismissed'),
                                     'X0003': CaseDetails.case_x(arrest_date=self.ONE_YEAR_AGO.strftime('%m/%d/%Y'),
                                                                 dispo_ruling_1='No Complaint',
                                                                 dispo_ruling_2='Convicted',
                                                                 dispo_ruling_3='No Complaint')})
        expunger = Expunger(self.crawler.result.cases)

        assert expunger.run() is True

        assert expunger._time_analyzer._most_recent_conviction.date == self.ONE_YEAR_AGO
        assert expunger._time_analyzer._second_most_recent_conviction.date == self.TWO_YEARS_AGO
        assert expunger._time_analyzer._most_recent_dismissal.date == self.ONE_YEAR_AGO
        assert expunger._time_analyzer._num_acquittals == 4

    def test_expunger_invokes_time_analyzer_with_most_recent_charge(self):
        CrawlerFactory.create(self.crawler,
                              cases={'X0001': CaseDetails.case_x(arrest_date=self.FIFTEEN_YEARS_AGO.strftime('%m/%d/%Y'),
                                                                 charge1_name='Aggravated theft in the first degree',
                                                                 charge1_statute='164.057',
                                                                 charge1_level='Felony Class B',
                                                                 dispo_ruling_1='Convicted',
                                                                 dispo_date=self.FIFTEEN_YEARS_AGO.strftime('%m/%d/%Y')),
                                     'X0002': CaseDetails.case_x(),
                                     'X0003': CaseDetails.case_x()})

        expunger = Expunger(self.crawler.result.cases)
        expunger.run()

        assert len(expunger._type_analyzer.class_b_felonies) == 1
        assert expunger._type_analyzer.class_b_felonies[0].name == 'Aggravated theft in the first degree'
        assert expunger._time_analyzer._class_b_felonies[0].name == 'Aggravated theft in the first degree'
        assert expunger._time_analyzer._most_recent_charge.name == 'Aggravated theft in the first degree'

    def test_expunger_expunges(self):
        CrawlerFactory.create(self.crawler,
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
        expunger = Expunger(self.crawler.result.cases)

        assert expunger.run() is True

        assert expunger._most_recent_conviction is None
        assert expunger._second_most_recent_conviction is None
        assert expunger._most_recent_dismissal.disposition.ruling == 'No Complaint'
        assert len(expunger._acquittals) == 8

        assert expunger.cases[0].charges[0].expungement_result.type_eligibility is True
        assert expunger.cases[0].charges[0].expungement_result.time_eligibility is False
        assert expunger.cases[0].charges[1].expungement_result.type_eligibility is False
        assert expunger.cases[0].charges[1].expungement_result.time_eligibility is False
        assert expunger.cases[0].charges[2].expungement_result.type_eligibility is True
        assert expunger.cases[0].charges[2].expungement_result.time_eligibility is False

        assert expunger.cases[1].charges[0].expungement_result.type_eligibility is True
        assert expunger.cases[1].charges[0].expungement_result.time_eligibility is False
        assert expunger.cases[1].charges[1].expungement_result.type_eligibility is True
        assert expunger.cases[1].charges[1].expungement_result.time_eligibility is False
        assert expunger.cases[1].charges[2].expungement_result.type_eligibility is True
        assert expunger.cases[1].charges[2].expungement_result.time_eligibility is False

        assert expunger.cases[2].charges[0].expungement_result.type_eligibility is True
        assert expunger.cases[2].charges[0].expungement_result.time_eligibility is True
        assert expunger.cases[2].charges[1].expungement_result.type_eligibility is True
        assert expunger.cases[2].charges[1].expungement_result.time_eligibility is True
        assert expunger.cases[2].charges[2].expungement_result.type_eligibility is True
        assert expunger.cases[2].charges[2].expungement_result.time_eligibility is True
