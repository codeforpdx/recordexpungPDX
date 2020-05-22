from typing import List, Any, Callable, Tuple
from datetime import datetime, date

from expungeservice.models.case import OeciCase, CaseSummary
from expungeservice.models.charge import OeciCharge
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.record import Record
from expungeservice.models.disposition import Disposition, DispositionStatus, DispositionCreator
from expungeservice.record_creator import RecordCreator


case_1 = OeciCase(
    CaseSummary(
        name="John Doe",
        birth_year=1980,
        case_number="X0001",
        citation_number="X0001",
        location="earth",
        date=date(2001, 1, 1),
        violation_type="Something",
        current_status="CLOSED",
        case_detail_link="alink",
        balance_due_in_cents=0,
    ),
    (
        OeciCharge(
            ambiguous_charge_id="X0001-1",
            name="manufacturing",
            statute="100.000",
            level="Felony Class B",
            date=date(2000, 1, 1),
            disposition=Disposition(
                date=date(2001, 1, 1), ruling="Convicted", status=DispositionStatus.CONVICTED, amended=False,
            ),
            probation_revoked=None,
        ),
        OeciCharge(
            ambiguous_charge_id="X0001-2",
            name="assault 3",
            statute="200.000",
            level="Felony Class C",
            date=date(2001, 1, 1),
            disposition=DispositionCreator.empty(),
            probation_revoked=None,
        ),
    ),
)
case_2 = OeciCase(
    CaseSummary(
        name="John Albert Doe",
        birth_year=1970,
        case_number="X0002",
        citation_number="X0002",
        location="america",
        date=date(2001, 1, 1),
        violation_type="Something Else",
        current_status="CLOSED",
        case_detail_link="alink",
        balance_due_in_cents=0,
    ),
    (
        OeciCharge(
            ambiguous_charge_id="X0002-1",
            name="driving",
            statute="100.000",
            level="Misdemeanor",
            date=date(2000, 1, 1),
            disposition=Disposition(
                date=date(2001, 1, 1), ruling="Convicted", status=DispositionStatus.CONVICTED, amended=False,
            ),
            probation_revoked=None,
        ),
        OeciCharge(
            ambiguous_charge_id="X0002-2",
            name="assault 3",
            statute="200.000",
            level="Violation",
            date=date(2001, 1, 1),
            disposition=DispositionCreator.empty(),
            probation_revoked=None,
        ),
    ),
)
mock_search_results = {"empty": [], "single_case_two_charges": [case_1], "two_cases_two_charges_each": [case_1, case_2]}


def search(mocked_record_name) -> Callable[[Any, Any, Any], Tuple[List[OeciCase], List[str]]]:
    def _build_search_results(username, password, aliases):
        return mock_search_results[mocked_record_name], []

    return _build_search_results


def test_no_op():
    record, ambiguous_record, questions, _ = RecordCreator.build_record(
        search("two_cases_two_charges_each"), "username", "password", (), {}
    )
    assert len(record.cases) == 2
    assert len(record.cases[0].charges) == 2
    assert record.cases[0].charges[1].disposition.status == DispositionStatus.UNKNOWN

def test_edit_some_fields_on_case():
    record, ambiguous_record, questions, _ = RecordCreator.build_record(
        search("two_cases_two_charges_each"),
        "username",
        "password",
        (),
        {"X0002": {"action": "edit", "summary": {"location": "ocean", "balance_due": "100", "date": "1/1/1001",}}},
    )
    assert len(record.cases) == 2
    assert record.cases[0].summary.location == "earth"
    assert record.cases[1].summary.location == "ocean"
    assert record.cases[1].summary.balance_due_in_cents == 10000
    assert record.cases[1].summary.date == date(1001, 1, 1)


def test_delete_case():
    record, ambiguous_record, questions, _ = RecordCreator.build_record(
        search("single_case_two_charges"), "username", "password", (), {"X0001": {"action": "delete"}},
    )
    assert record == Record((), ())


def test_add_disposition():
    record, ambiguous_record, questions, _ = RecordCreator.build_record(
        search("single_case_two_charges"),
        "username",
        "password",
        (),
        {
            "X0001": {
                "action": "edit",
                "charges": {"X0001-2": {"disposition": {"date": "1/1/2001", "ruling": "Convicted"}}},
            }
        },
    )
    assert record.cases[0].charges[1].disposition.status == DispositionStatus.CONVICTED


def test_edit_charge_type_of_charge():
    record, ambiguous_record, questions, _ = RecordCreator.build_record(
        search("single_case_two_charges"),
        "username",
        "password",
        (),
        {"X0001": {"action": "edit", "charges": {"X0001-2": {"charge_type": "Misdemeanor"}},}},
    )
    assert isinstance(record.cases[0].charges[1], Misdemeanor)


def test_add_new_charge():
    record, ambiguous_record, questions, _ = RecordCreator.build_record(
        search("single_case_two_charges"),
        "username",
        "password",
        (),
        {
            "X0001": {
                "action": "edit",
                "charges": {
                    "X0001-3": {
                        "charge_type": "Misdemeanor",
                        "date": "1/1/2001",
                        "disposition": {"date": "2/1/2001", "ruling": "Convicted"},
                    }
                },
            }
        },
    )
    assert isinstance(record.cases[0].charges[2], Misdemeanor)
    assert record.cases[0].charges[2].date == date(2001, 1, 1)


def test_add_new_case():
    record, ambiguous_record, questions, _ = RecordCreator.build_record(
        search("single_case_two_charges"),
        "username",
        "password",
        (),
        {
            "NEW-0001": {
                "action": "add",
                "summary": {
                    "balance_due_in_cents": 0,
                    "location": "sky",
                    "date":"1/1/1990"
                },
            }
        },
    )

    assert len(record.cases)==2
    assert record.cases[0].summary.case_number=="X0001"
    assert record.cases[0].summary.location=="earth"

    assert record.cases[1].summary.case_number=="NEW-0001"
    assert record.cases[1].summary.balance_due_in_cents==0
    assert record.cases[1].summary.location=="sky"
    assert record.cases[1].summary.birth_year==0
