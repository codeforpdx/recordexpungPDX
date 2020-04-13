from expungeservice.record_creator import RecordCreator
from tests.factories.crawler_factory import CrawlerFactory
from tests.factories.case_factory import CaseFactory
import datetime


def test_ensure_unsorted():
    mock_data = CrawlerFactory.create()
    mock_cases = mock_data.cases
    assert mock_cases[0].date == datetime.date(1963, 3, 23)
    assert mock_cases[1].date == datetime.date(1963, 4, 11)
    assert mock_cases[2].date == datetime.date(2012, 4, 1)


def test_sort_by_case_date():
    mock_data = CrawlerFactory.create()
    sortedRecord = RecordCreator.sort_record_by_case_date(mock_data)
    sorted_mock_cases = sortedRecord.cases
    assert sorted_mock_cases[0].date == datetime.date(2012, 4, 1)
    assert sorted_mock_cases[1].date == datetime.date(1963, 4, 11)
    assert sorted_mock_cases[2].date == datetime.date(1963, 3, 23)


def test_sort_if_all_dates_are_same():
    mock_data = CrawlerFactory.create()
    mock_cases = mock_data.cases
    mock_cases[0].date = datetime.date(1963, 3, 23)
    mock_cases[1].date = datetime.date(1963, 3, 23)
    mock_cases[2].date = datetime.date(1963, 3, 23)

    assert mock_cases[0].case_number == "X0001"
    assert mock_cases[1].case_number == "X0002"
    assert mock_cases[2].case_number == "X0003"

    sortedData = RecordCreator.sort_record_by_case_date(mock_data)
    sortedCases = sortedData.cases

    # data should be untouched
    assert sortedCases[0].case_number == "X0001"
    assert sortedCases[1].case_number == "X0002"
    assert sortedCases[2].case_number == "X0003"
