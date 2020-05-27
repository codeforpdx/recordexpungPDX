from expungeservice.models.disposition import DispositionStatus
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe
from expungeservice.models.record import Record
from expungeservice.util import DateWithFuture as date_class


def test_search_function():
    record = CrawlerFactory.create(
        JohnDoe.RECORD,
        {
            "X0001": CaseDetails.CASE_X1,
            "X0002": CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
            "X0003": CaseDetails.CASE_WITHOUT_DISPOS,
        },
    )
    # sorting by date results in the order X0003, X0002, X0001
    assert record.__class__ == Record
    assert len(record.cases) == 3

    assert len(record.cases[2].charges) == 3
    assert len(record.cases[1].charges) == 1
    assert len(record.cases[0].charges) == 3

    assert record.cases[2].charges[0].disposition.ruling == "Convicted - Failure to Appear"
    assert record.cases[2].charges[0].disposition.date == date_class(2017, 6, 12)
    assert record.cases[2].charges[1].disposition.ruling == "Dismissed"
    assert record.cases[2].charges[1].disposition.date == date_class(2017, 6, 12)
    assert record.cases[2].charges[2].disposition.ruling == "Dismissed"
    assert record.cases[2].charges[2].disposition.date == date_class(2017, 6, 12)

    assert record.cases[1].charges[0].disposition.ruling == "Dismissed"
    assert record.cases[1].charges[0].disposition.date == date_class(1992, 4, 30)

    assert record.cases[0].charges[0].disposition.status == DispositionStatus.UNKNOWN
    assert record.cases[0].charges[0].disposition.status == DispositionStatus.UNKNOWN
    assert record.cases[0].charges[1].disposition.status == DispositionStatus.UNKNOWN
    assert record.cases[0].charges[1].disposition.status == DispositionStatus.UNKNOWN
    assert record.cases[0].charges[2].disposition.status == DispositionStatus.UNKNOWN
    assert record.cases[0].charges[2].disposition.status == DispositionStatus.UNKNOWN


def test_a_blank_search_response():
    record = CrawlerFactory.create(JohnDoe.BLANK_RECORD, {})

    assert len(record.cases) == 0


def test_single_charge_conviction():
    record = CrawlerFactory.create(JohnDoe.SINGLE_CASE_RECORD, {"CASEJD1": CaseDetails.CASEJD1})

    assert len(record.cases) == 1
    assert len(record.cases[0].charges) == 1

    assert record.cases[0].charges[0].name == "Loading Zone"
    assert record.cases[0].charges[0].statute == "29"
    assert record.cases[0].charges[0].level == "Violation Unclassified"
    assert record.cases[0].charges[0].date == date_class(2008, 9, 4)
    assert record.cases[0].charges[0].disposition.ruling == "Convicted"
    assert record.cases[0].charges[0].disposition.date == date_class(2008, 11, 18)


def test_nonzero_balance_due_on_case():
    record = CrawlerFactory.create(
        JohnDoe.RECORD,
        {
            "X0001": CaseDetails.CASE_X1,
            "X0002": CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
            "X0003": CaseDetails.CASE_WITHOUT_DISPOS,
        },
    )

    assert record.cases[2].summary.get_balance_due() == 1516.80


def test_zero_balance_due_on_case():
    record = CrawlerFactory.create(JohnDoe.SINGLE_CASE_RECORD, {"CASEJD1": CaseDetails.CASEJD1})

    assert record.cases[0].summary.get_balance_due() == 0
