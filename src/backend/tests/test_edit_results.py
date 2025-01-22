from typing import List, Any, Callable, Tuple
from expungeservice.util import DateWithFuture as date, LRUCache
from expungeservice.models.case import OeciCase, CaseSummary
from expungeservice.models.charge import OeciCharge, EditStatus
from expungeservice.models.charge_types.misdemeanor_class_a import MisdemeanorClassA
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.record import Record
from expungeservice.models.disposition import Disposition, DispositionStatus, DispositionCreator
from expungeservice.models.expungement_result import ChargeEligibilityStatus, EligibilityStatus
from expungeservice.record_creator import RecordCreator

case_1 = OeciCase(
    CaseSummary(
        name="John Doe",
        birth_year=1980,
        case_number="X0001",
        district_attorney_number="555",
        sid="OR12345678",
        citation_number="X0001",
        location="earth",
        date=date(2001, 1, 1),
        violation_type="Something",
        current_status="CLOSED",
        case_detail_link="alink",
        balance_due_in_cents=0,
        restitution=False,
        edit_status=EditStatus.UNCHANGED,
    ),
    (
        OeciCharge(
            ambiguous_charge_id="X0001-1",
            name="petty theft",
            statute="100.000",
            level="Misdemeanor",
            date=date(2000, 1, 1),
            disposition=Disposition(
                date=date(2001, 1, 1),
                ruling="Convicted",
                status=DispositionStatus.CONVICTED,
                amended=False,
            ),
            probation_revoked=None,
            balance_due_in_cents=0,
            edit_status=EditStatus.UNCHANGED,
        ),
        OeciCharge(
            ambiguous_charge_id="X0001-2",
            name="assault 3",
            statute="200.000",
            level="Felony Class C",
            date=date(2001, 1, 1),
            disposition=Disposition(
                date=date(2001, 1, 1),
                ruling="Convicted",
                status=DispositionStatus.CONVICTED,
                amended=False,
            ),
            probation_revoked=None,
            balance_due_in_cents=0,
            edit_status=EditStatus.UNCHANGED,
        ),
    ),
)
case_2 = OeciCase(
    CaseSummary(
        name="John Albert Doe",
        birth_year=1970,
        case_number="X0002",
        district_attorney_number="555",
        sid="OR12345678",
        citation_number="X0002",
        location="america",
        date=date(1981, 1, 1),
        violation_type="Something Else",
        current_status="CLOSED",
        case_detail_link="alink",
        balance_due_in_cents=0,
        restitution=False,
        edit_status=EditStatus.UNCHANGED,
    ),
    (
        OeciCharge(
            ambiguous_charge_id="X0002-1",
            name="something class B",
            statute="100.000",
            level="Felony Class B",
            date=date(1980, 1, 1),
            disposition=Disposition(
                date=date(1981, 1, 1),
                ruling="Convicted",
                status=DispositionStatus.CONVICTED,
                amended=False,
            ),
            probation_revoked=None,
            balance_due_in_cents=0,
            edit_status=EditStatus.UNCHANGED,
        ),
        OeciCharge(
            ambiguous_charge_id="X0002-2",
            name="assault 3",
            statute="200.000",
            level="Violation",
            date=date(1001, 1, 1),
            disposition=DispositionCreator.empty(),
            probation_revoked=None,
            balance_due_in_cents=0,
            edit_status=EditStatus.UNCHANGED,
        ),
    ),
)
mock_search_results = {"empty": [], "single_case_two_charges": [case_1], "two_cases_two_charges_each": [case_1, case_2]}


def search(mocked_record_name) -> Callable[[Any, Any, Any, Any], Tuple[List[OeciCase], List[str]]]:
    def _build_search_results(username, password, aliases, lru_cache):
        return mock_search_results[mocked_record_name], []

    return _build_search_results


def test_no_op():
    record, questions = RecordCreator.build_record(
        search("two_cases_two_charges_each"), "username", "password", (), {}, date.today(), LRUCache(4)
    )
    assert len(record.cases) == 2
    assert len(record.cases[0].charges) == 2
    assert record.cases[1].charges[1].ambiguous_charge_id == "X0002-2"
    assert record.cases[1].charges[1].disposition.status == DispositionStatus.UNKNOWN
    assert record.cases[1].summary.edit_status == EditStatus.UNCHANGED
    assert isinstance(record.cases[1].charges[0].charge_type, FelonyClassB)
    assert (
        record.cases[1].charges[0].expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
    )
    assert record.cases[1].charges[0].expungement_result.time_eligibility.status == EligibilityStatus.ELIGIBLE


def test_edit_some_fields_on_case():
    record, questions = RecordCreator.build_record(
        search("two_cases_two_charges_each"),
        "username",
        "password",
        (),
        {
            "X0002": {
                "summary": {
                    "edit_status": "UPDATE",
                    "location": "ocean",
                    "balance_due": "100",
                    "date": "1/1/1981",
                }
            }
        },
        date.today(),
        LRUCache(4),
    )
    assert len(record.cases) == 2
    assert record.cases[0].summary.location == "earth"
    assert record.cases[0].summary.edit_status == EditStatus.UNCHANGED
    assert record.cases[1].summary.location == "ocean"
    assert record.cases[1].summary.balance_due_in_cents == 10000
    assert record.cases[1].summary.date == date(1981, 1, 1)
    assert record.cases[1].summary.edit_status == EditStatus.UPDATE


def test_delete_case():
    record, questions = RecordCreator.build_record(
        search("two_cases_two_charges_each"),
        "username",
        "password",
        (),
        {"X0001": {"summary": {"edit_status": "DELETE"}}},
        date.today(),
        LRUCache(4),
    )

    assert record.cases[0].summary.case_number == "X0001"
    assert record.cases[0].summary.edit_status == EditStatus.DELETE
    assert len(record.cases[0].charges) == 2
    assert record.cases[0].charges[0].edit_status == EditStatus.DELETE
    assert record.cases[0].charges[1].edit_status == EditStatus.DELETE
    assert record.cases[1].summary.case_number == "X0002"
    assert record.cases[1].summary.edit_status == EditStatus.UNCHANGED


def test_add_case():
    record, questions = RecordCreator.build_record(
        search("single_case_two_charges"),
        "username",
        "password",
        (),
        {
            "5": {
                "summary": {
                    "case_number": "5",
                    "edit_status": "ADD",
                    "location": "ocean",
                    "balance_due": "100",
                    "date": "1/1/1981",
                },
                "charges": {
                    "5-1": {
                        "edit_status": "ADD",
                        "charge_type": "FelonyClassC",
                        "level": "Felony Class C",
                        "date": "1/1/2001",
                        "disposition": {"date": "2/1/2020", "ruling": "Convicted"},
                    }
                },
            }
        },
        date.today(),
        LRUCache(4),
    )
    assert len(record.cases) == 2
    assert record.cases[0].summary.location == "earth"
    assert record.cases[0].summary.edit_status == EditStatus.UNCHANGED

    assert record.cases[1].summary.location == "ocean"
    assert record.cases[1].summary.balance_due_in_cents == 10000
    assert record.cases[1].summary.date == date(1981, 1, 1)
    assert record.cases[1].summary.edit_status == EditStatus.ADD
    assert record.cases[1].charges[0].edit_status == EditStatus.ADD
    assert record.cases[1].charges[0].charge_type
    assert isinstance(record.cases[1].charges[0].charge_type, FelonyClassC)


def test_update_case_with_add_and_update_and_delete_charges():
    record, questions = RecordCreator.build_record(
        search("single_case_two_charges"),
        "username",
        "password",
        (),
        {
            "X0001": {
                "summary": {
                    "case_number": "X0001",
                    "edit_status": "UPDATE",
                    "location": "ocean",
                    "balance_due": "100",
                    "date": "1/1/1981",
                },
                "charges": {
                    "X0001-1": {
                        "edit_status": "UPDATE",
                        "charge_type": "FelonyClassB",
                        "level": "Felony Class B",
                        "date": "1/1/2001",
                        "disposition": {"date": "2/1/2020", "ruling": "Convicted"},
                    },
                    "X0001-2": {"edit_status": "DELETE"},
                    "X0001-3": {
                        "edit_status": "ADD",
                        "charge_type": "FelonyClassC",
                        "date": "1/1/1900",
                        "level": "Felony Class A",
                        "disposition": {"date": "2/1/1910", "ruling": "Convicted"},
                    },
                },
            }
        },
        date.today(),
        LRUCache(4),
    )
    assert len(record.cases) == 1
    assert record.cases[0].summary.location == "ocean"
    assert record.cases[0].summary.edit_status == EditStatus.UPDATE
    assert record.cases[0].charges[0].ambiguous_charge_id == "X0001-1"
    assert record.cases[0].charges[0].edit_status == EditStatus.UPDATE
    assert isinstance(record.cases[0].charges[0].charge_type, FelonyClassB)
    assert record.cases[0].charges[1].ambiguous_charge_id == "X0001-2"
    assert record.cases[0].charges[1].edit_status == EditStatus.DELETE
    assert record.cases[0].charges[2].ambiguous_charge_id == "X0001-3"
    assert record.cases[0].charges[2].edit_status == EditStatus.ADD


def test_add_disposition():
    record, questions = RecordCreator.build_record(
        search("single_case_two_charges"),
        "username",
        "password",
        (),
        {
            "X0001": {
                "summary": {"edit_status": "UPDATE"},
                "charges": {
                    "X0001-2": {
                        "disposition": {"date": "1/1/2001", "ruling": "Convicted"},
                        "level": "Misdemeanor Class A",
                    }
                },
            }
        },
        date.today(),
        LRUCache(4),
    )
    assert record.cases[0].charges[1].disposition.status == DispositionStatus.CONVICTED
    assert record.cases[0].charges[1].edit_status == EditStatus.UNCHANGED


def test_edit_charge_type_of_charge():
    record, questions = RecordCreator.build_record(
        search("single_case_two_charges"),
        "username",
        "password",
        (),
        {
            "X0001": {
                "summary": {"edit_status": "UPDATE"},
                "charges": {
                    "X0001-2": {
                        "edit_status": "UPDATE",
                        "charge_type": "MisdemeanorClassA",
                        "level": "Misdemeanor Class A",
                    }
                },
            }
        },
        date.today(),
        LRUCache(4),
    )
    assert isinstance(record.cases[0].charges[1].charge_type, MisdemeanorClassA)


def test_add_new_charge():
    record, questions = RecordCreator.build_record(
        search("single_case_two_charges"),
        "username",
        "password",
        (),
        {
            "X0001": {
                "summary": {"edit_status": "UPDATE"},
                "charges": {
                    "X0001-3": {
                        "edit_status": "ADD",
                        "charge_type": "MisdemeanorClassA",
                        "level": "Misdemeanor Class A",
                        "date": "1/1/2001",
                        "disposition": {"date": "2/1/2020", "ruling": "Convicted"},
                    }
                },
            }
        },
        date.today(),
        LRUCache(4),
    )
    assert isinstance(record.cases[0].charges[2].charge_type, MisdemeanorClassA)
    assert record.cases[0].charges[2].date == date(2001, 1, 1)
    assert record.cases[0].charges[2].edit_status == EditStatus.ADD


def test_deleted_charge_does_not_block():
    """"""
    record, questions = RecordCreator.build_record(
        search("two_cases_two_charges_each"),
        "username",
        "password",
        (),
        {
            "X0001": {
                "summary": {"edit_status": "UPDATE"},
                "charges": {
                    "X0001-1": {
                        "edit_status": "UPDATE",
                        "date": "1/1/2020",
                        "disposition": {"date": "2/1/2020", "ruling": "Convicted"},
                        "level": "Misdemeanor Class A",
                    }
                },
            },
        },
        date.today(),
        LRUCache(4),
    )
    assert record.cases[0].summary.case_number == "X0001"
    assert record.cases[0].summary.edit_status == EditStatus.UPDATE
    assert record.cases[0].charges[0].edit_status == EditStatus.UPDATE
    assert record.cases[0].charges[1].edit_status == EditStatus.UNCHANGED

    assert record.cases[1].summary.case_number == "X0002"
    assert (
        record.cases[1].charges[0].expungement_result.charge_eligibility.status
        == ChargeEligibilityStatus.WILL_BE_ELIGIBLE
    )

    record, questions = RecordCreator.build_record(
        search("two_cases_two_charges_each"),
        "username",
        "password",
        (),
        {
            "X0001": {
                "summary": {
                    "edit_status": "UPDATE",
                },
                "charges": {
                    "X0001-1": {"edit_status": "DELETE"},
                    "X0001-2": {"edit_status": "DELETE"},
                },
            }
        },
        date.today(),
        LRUCache(4),
    )

    assert record.cases[0].summary.case_number == "X0001"
    assert record.cases[0].summary.edit_status == EditStatus.UPDATE
    assert record.cases[0].charges[0].edit_status == EditStatus.DELETE
    assert record.cases[0].charges[1].edit_status == EditStatus.DELETE

    assert record.cases[1].summary.case_number == "X0002"
    assert (
        record.cases[1].charges[0].expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
    )


# More thoughts on using / testing Edits:
# Edits to a case MUST include "case_number": {"summary":{"edit_status":[something]}}. Without the edit_status it will break.
# Edits to an existing charge don't need to include edit_status. This allows the frontend to edit the disposition (answering a  DispositionQuestion) without adding the UPDATED badge.
# If an ambiguous_charge_id isn't recognized, its edit_status must be ADD. Otherwise it will break
# If a new charge is being added, the charge_type must be provided. Otherwise it will break. there is no check for this.
