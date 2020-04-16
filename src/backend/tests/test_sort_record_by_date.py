from expungeservice.record_creator import RecordCreator
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory


def test_sort_by_case_date():
    case1 = CaseFactory.create(case_number="1", date_location=["1/1/2018", "Multnomah"])
    case2 = CaseFactory.create(case_number="2", date_location=["1/1/2019", "Multnomah"])
    case3 = CaseFactory.create(case_number="3", date_location=["1/1/2020", "Multnomah"])

    record = Record(tuple([case1, case2, case3]))
    assert record.cases[0].case_number == "1"
    assert record.cases[1].case_number == "2"
    assert record.cases[2].case_number == "3"

    sorted_record = RecordCreator.sort_record_by_case_date(record)
    assert sorted_record.cases[0].case_number == "3"
    assert sorted_record.cases[1].case_number == "2"
    assert sorted_record.cases[2].case_number == "1"


def test_sort_if_all_dates_are_same():
    case1 = CaseFactory.create(case_number="1")
    case2 = CaseFactory.create(case_number="2")
    case3 = CaseFactory.create(case_number="3")

    record = Record(tuple([case1, case2, case3]))
    assert record.cases[0].case_number == "1"
    assert record.cases[1].case_number == "2"
    assert record.cases[2].case_number == "3"

    sorted_record = RecordCreator.sort_record_by_case_date(record)
    assert sorted_record.cases[0].case_number == "1"
    assert sorted_record.cases[1].case_number == "2"
    assert sorted_record.cases[2].case_number == "3"
