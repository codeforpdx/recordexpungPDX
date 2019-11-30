from datetime import date as date_class

import pytest
from dateutil.relativedelta import relativedelta
from expungeservice.expunger.expunger import Expunger
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe

ONE_YEAR_AGO = (date_class.today() + relativedelta(years=-1))
TWO_YEARS_AGO = (date_class.today() + relativedelta(years=-2))
FIFTEEN_YEARS_AGO = (date_class.today() + relativedelta(years=-15))


@pytest.fixture
def crawler():
    return CrawlerFactory.setup()


@pytest.fixture
def record_with_open_case(crawler):
    return CrawlerFactory.create(crawler, JohnDoe.RECORD,
                                 {'X0001': CaseDetails.CASE_X1,
                                  'X0002': CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
                                  'X0003': CaseDetails.CASE_WITHOUT_DISPOS})


def test_expunger_with_open_case(record_with_open_case):
    expunger = Expunger(record_with_open_case)

    assert not expunger.run()
    assert expunger.errors == ['Open cases exist']


@pytest.fixture
def empty_record(crawler):
    return CrawlerFactory.create(crawler, JohnDoe.BLANK_RECORD, {})


def test_expunger_with_an_empty_record(empty_record):
    expunger = Expunger(empty_record)

    assert expunger.run()
    assert expunger.most_recent_dismissal is None
    assert expunger.most_recent_conviction is None


@pytest.fixture
def partial_dispos_record(crawler):
    return CrawlerFactory.create(crawler, JohnDoe.SINGLE_CASE_RECORD,
                                 {'CASEJD1': CaseDetails.CASE_WITH_PARTIAL_DISPOS})


def test_partial_dispos(partial_dispos_record):
    expunger = Expunger(partial_dispos_record)
    assert expunger.run()


@pytest.fixture
def record_without_dispos(crawler):
    return CrawlerFactory.create(crawler, JohnDoe.SINGLE_CASE_RECORD,
                                 {'CASEJD1': CaseDetails.CASE_WITHOUT_DISPOS})


def test_case_without_dispos(record_without_dispos):
    expunger = Expunger(record_without_dispos)
    assert expunger.run()


@pytest.fixture
def record_with_various_categories(crawler):
    return CrawlerFactory.create(crawler,
                                 cases={'X0001': CaseDetails.case_x(
                                     dispo_ruling_1='Convicted - Failure to show',
                                     dispo_ruling_2='Dismissed',
                                     dispo_ruling_3='Acquitted'),
                                     'X0002': CaseDetails.case_x(
                                         dispo_ruling_1='Dismissed',
                                         dispo_ruling_2='Convicted',
                                         dispo_ruling_3='Convicted'),
                                     'X0003': CaseDetails.case_x(
                                         dispo_ruling_1='No Complaint',
                                         dispo_ruling_2='Dismissed',
                                         dispo_ruling_3='Convicted')})


def test_expunger_categorizes_charges(record_with_various_categories):
    expunger = Expunger(record_with_various_categories)

    assert expunger.run()
    assert len(expunger.acquittals) == 5
    assert len(expunger.convictions) == 4

@pytest.fixture
def record_with_specific_dates(crawler):
    return CrawlerFactory.create(crawler,
                                   cases={'X0001': CaseDetails.case_x(
                                       arrest_date=FIFTEEN_YEARS_AGO.strftime(
                                           '%m/%d/%Y'),
                                       dispo_date=FIFTEEN_YEARS_AGO.strftime(
                                           '%m/%d/%Y'),
                                       dispo_ruling_1='Dismissed',
                                       dispo_ruling_2='Convicted',
                                       dispo_ruling_3='Acquitted'),
                                          'X0002': CaseDetails.case_x(
                                              arrest_date=TWO_YEARS_AGO.strftime(
                                                  '%m/%d/%Y'),
                                              dispo_ruling_1='Dismissed',
                                              dispo_ruling_2='Dismissed',
                                              dispo_ruling_3='Dismissed'),
                                          'X0003': CaseDetails.case_x(
                                              arrest_date=ONE_YEAR_AGO.strftime(
                                                  '%m/%d/%Y'),
                                              dispo_ruling_1='No Complaint',
                                              dispo_ruling_2='No Complaint',
                                              dispo_ruling_3='No Complaint')})

def test_expunger_runs_time_analyzer(record_with_specific_dates):
    record = record_with_specific_dates
    expunger = Expunger(record)

    assert expunger.run()

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
