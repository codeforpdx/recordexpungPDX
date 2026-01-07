from expungeservice.models.case import Case
from expungeservice.util import DateWithFuture as date

import pytest
from dateutil.relativedelta import relativedelta
from expungeservice.expunger import Expunger
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaUnder21
from expungeservice.models.charge_types.civil_offense import CivilOffense
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.felony_class_a import FelonyClassA

from expungeservice.models.expungement_result import EligibilityStatus, TimeEligibility
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe
from tests.fixtures.young_doe import YoungDoe

ONE_YEAR_AGO = date.today() + relativedelta(years=-1)
TWO_YEARS_AGO = date.today() + relativedelta(years=-2)
FIFTEEN_YEARS_AGO = date.today() + relativedelta(years=-15)


@pytest.fixture
def record_with_open_case():
    return CrawlerFactory.create(
        JohnDoe.RECORD,
        {
            "X0001": CaseDetails.CASE_X1,
            "X0002": CaseDetails.CASE_WITHOUT_FINANCIAL_SECTION,
            "X0003": CaseDetails.CASE_WITHOUT_DISPOS,
        },
    )


def test_expunger_with_open_case(record_with_open_case):
    errors = record_with_open_case.errors
    expunger_result = Expunger.run(record_with_open_case)

    assert len(expunger_result) == 4
    assert "All charges are ineligible because there is one or more open case" in errors[0]


@pytest.fixture
def empty_record():
    return CrawlerFactory.create(JohnDoe.BLANK_RECORD, {})


def test_expunger_with_an_empty_record(empty_record):
    expunger_result = Expunger.run(empty_record)
    assert expunger_result == {}


@pytest.fixture
def partial_dispos_record():
    return CrawlerFactory.create(JohnDoe.SINGLE_CASE_RECORD, {"CASEJD1": CaseDetails.CASE_WITH_PARTIAL_DISPOS})


def test_partial_dispos(partial_dispos_record):
    expunger_result = Expunger.run(partial_dispos_record)
    assert len(expunger_result) == 1


@pytest.fixture
def record_without_dispos():
    return CrawlerFactory.create(JohnDoe.SINGLE_CASE_RECORD, {"CASEJD1": CaseDetails.CASE_WITHOUT_DISPOS})


def test_case_without_dispos(record_without_dispos):
    errors = record_without_dispos.errors
    expunger_result = Expunger.run(record_without_dispos)
    assert record_without_dispos.cases[0].summary.closed()
    assert expunger_result == {}
    assert errors[0] == (
        f"""Case [{record_without_dispos.cases[0].summary.case_number}] has a charge with a missing disposition.
This might be an error in the OECI database. Time analysis is ignoring this charge and may be inaccurate for other charges."""
    )


@pytest.fixture
def record_with_unrecognized_dispo():
    return CrawlerFactory.create(
        cases={
            "X0001": CaseDetails.case_x(dispo_ruling_1="Something unrecognized"),
            "X0002": CaseDetails.case_x(dispo_ruling_1="Something unrecognized"),
            "X0003": CaseDetails.case_x(dispo_ruling_1="Something unrecognized"),
        },
    )


def test_case_with_unrecognized_dispo(record_with_unrecognized_dispo):
    errors = record_with_unrecognized_dispo.errors
    expunger_result = Expunger.run(record_with_unrecognized_dispo)
    assert len(expunger_result) == 6
    assert "The following cases have charges with an unrecognized disposition" in errors[0]


@pytest.fixture
def record_with_multiple_disposition_errors():
    return CrawlerFactory.create(
        cases={
            "X0001": CaseDetails.case_x(dispo_ruling_1="Something unrecognized"),
            "X0002": CaseDetails.case_x(dispo_ruling_1="Something else unrecognized"),
            "X0003": CaseDetails.CASE_WITHOUT_DISPOS,
        },
    )


def test_case_with_mulitple_disposition_errors(record_with_multiple_disposition_errors):
    errors = record_with_multiple_disposition_errors.errors
    unrecognized_error_message = f"""The following cases have charges with an unrecognized disposition.
This might be an error in the OECI database. Time analysis is ignoring these charges and may be inaccurate for other charges.
Case numbers: """
    cases_order_1 = "[X0001] (Something unrecognized), [X0002] (Something else unrecognized)"
    cases_order_2 = "[X0002] (Something else unrecognized), [X0001] (Something unrecognized)"
    assert unrecognized_error_message + cases_order_1 in errors or unrecognized_error_message + cases_order_2 in errors
    missing_error_message = f"""Case [X0003] has a charge with a missing disposition.
This might be an error in the OECI database. Time analysis is ignoring this charge and may be inaccurate for other charges."""
    assert missing_error_message in errors


@pytest.fixture
def record_with_various_categories():
    return CrawlerFactory.create(
        cases={
            "X0001": CaseDetails.case_x(
                dispo_ruling_1="Convicted - Failure to show", dispo_ruling_2="Dismissed", dispo_ruling_3="Acquitted"
            ),
            "X0002": CaseDetails.case_x(
                dispo_ruling_1="Dismissed", dispo_ruling_2="Convicted", dispo_ruling_3="Convicted"
            ),
            "X0003": CaseDetails.case_x(
                dispo_ruling_1="No Complaint", dispo_ruling_2="Dismissed", dispo_ruling_3="Convicted"
            ),
        },
    )


def test_expunger_categorizes_charges(record_with_various_categories):
    dismissals, convictions = Case.categorize_charges(record_with_various_categories.charges)

    assert len(dismissals) == 5
    assert len(convictions) == 4


@pytest.fixture
def record_with_specific_dates():
    return CrawlerFactory.create(
        cases={
            "X0001": CaseDetails.case_x(
                arrest_date=FIFTEEN_YEARS_AGO.strftime("%m/%d/%Y"),
                dispo_date=FIFTEEN_YEARS_AGO.strftime("%m/%d/%Y"),
                dispo_ruling_1="Dismissed",
                dispo_ruling_2="Convicted",
                dispo_ruling_3="Acquitted",
            ),
            "X0002": CaseDetails.case_x(
                arrest_date=TWO_YEARS_AGO.strftime("%m/%d/%Y"),
                dispo_ruling_1="Dismissed",
                dispo_ruling_2="Dismissed",
                dispo_ruling_3="Dismissed",
            ),
            "X0003": CaseDetails.case_x(
                arrest_date=ONE_YEAR_AGO.strftime("%m/%d/%Y"),
                dispo_ruling_1="No Complaint",
                dispo_ruling_2="No Complaint",
                dispo_ruling_3="No Complaint",
            ),
        },
    )


def test_expunger_runs_time_analyzer(record_with_specific_dates):
    record = record_with_specific_dates
    expunger_result = Expunger.run(record)

    assert len(expunger_result) == 9
    assert expunger_result[record.cases[0].charges[0].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[record.cases[0].charges[1].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[record.cases[0].charges[2].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE

    assert expunger_result[record.cases[1].charges[0].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[record.cases[1].charges[1].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[record.cases[1].charges[2].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE

    assert expunger_result[record.cases[2].charges[0].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[record.cases[2].charges[1].ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert expunger_result[record.cases[2].charges[2].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE


@pytest.fixture
def record_with_revoked_probation():
    return CrawlerFactory.create(
        cases={
            "X0001": CaseDetails.CASE_WITH_REVOKED_PROBATION,
            "X0002": CaseDetails.case_x(dispo_ruling_1="Something unrecognized"),
            "X0003": CaseDetails.case_x(dispo_ruling_1="Something unrecognized"),
        },
    )


def test_probation_revoked_affects_time_eligibility(record_with_revoked_probation):
    record = record_with_revoked_probation
    expunger_result = Expunger.run(record)

    assert len(expunger_result) == 6
    assert expunger_result[record.cases[2].charges[0].ambiguous_charge_id].date_will_be_eligible == date(2020, 11, 9)


@pytest.fixture
def record_with_odd_event_table_contents():
    return CrawlerFactory.create(
        record=JohnDoe.SINGLE_CASE_RECORD,
        cases={
            "CASEJD1": CaseDetails.CASE_WITH_ODD_EVENT_TABLE_CONTENTS,
        },
    )


def test_expunger_for_record_with_odd_event_table_contents(record_with_odd_event_table_contents):
    expunger_result = Expunger.run(record_with_odd_event_table_contents)
    assert expunger_result == {
        "CASEJD1-1": TimeEligibility(
            status=EligibilityStatus.INELIGIBLE,
            reason="Never. Type ineligible charges are always time ineligible.",
            date_will_be_eligible=date.max(),
        ),
        "CASEJD1-2": TimeEligibility(
            status=EligibilityStatus.INELIGIBLE,
            reason="Never. Type ineligible charges are always time ineligible.",
            date_will_be_eligible=date.max(),
        ),
    }


@pytest.fixture
def record_with_mj_under_21():
    return CrawlerFactory.create(
        record=YoungDoe.SINGLE_CASE_RECORD,
        cases={
            "CASEJD1": CaseDetails.CASE_MJ_CONVICTION,
        },
    )


def test_expunger_for_record_with_mj_under_21(record_with_mj_under_21):
    assert isinstance(record_with_mj_under_21.charges[0].charge_type, MarijuanaUnder21)
    expunger_result = Expunger.run(record_with_mj_under_21)
    assert expunger_result == {
        "CASEJD1-1": TimeEligibility(
            status=EligibilityStatus.ELIGIBLE, reason="Eligible now", date_will_be_eligible=date(1999, 3, 3)
        )
    }


@pytest.fixture
def record_with_mj_over_21():
    return CrawlerFactory.create(
        record=JohnDoe.SINGLE_CASE_RECORD,
        cases={
            "CASEJD1": CaseDetails.CASE_MJ_CONVICTION,
        },
    )


def test_expunger_for_record_with_mj_over_21(record_with_mj_over_21):
    expunger_result = Expunger.run(record_with_mj_over_21)
    assert expunger_result == {
        "CASEJD1-1": TimeEligibility(
            status=EligibilityStatus.ELIGIBLE, reason="Eligible now", date_will_be_eligible=date(2001, 3, 3)
        )
    }


@pytest.fixture
def record_with_mj_under_21_and_traffic_violation():
    return CrawlerFactory.create(
        record=YoungDoe.SINGLE_CASE_RECORD,
        cases={
            "CASEJD1": CaseDetails.CASE_MJ_AND_TRAFFIC_CONVICTION,
        },
    )


def test_expunger_for_record_with_mj_under_21_not_blocked_by_traffic(record_with_mj_under_21_and_traffic_violation):
    expunger_result = Expunger.run(record_with_mj_under_21_and_traffic_violation)
    mj_charge = record_with_mj_under_21_and_traffic_violation.charges[0]
    traffic_charge = record_with_mj_under_21_and_traffic_violation.charges[1]

    assert isinstance(mj_charge.charge_type, MarijuanaUnder21)
    assert isinstance(traffic_charge.charge_type, TrafficViolation)

    assert expunger_result["CASEJD1-1"] == TimeEligibility(
        status=EligibilityStatus.ELIGIBLE,
        reason="Eligible now",
        date_will_be_eligible=mj_charge.disposition.date + relativedelta(years=1),
    )


def test_expunger_for_record_with_mj_under_21_with_non_traffic_charge():
    record = CrawlerFactory.create(
        record=YoungDoe.SINGLE_CASE_RECORD, cases={"CASEJD1": CaseDetails.CASE_MJ_AND_FUGITIVE_CONVICTION}
    )

    expunger_result = Expunger.run(record)
    mj_charge = record.charges[0]

    assert isinstance(mj_charge.charge_type, MarijuanaUnder21)
    assert isinstance(record.charges[1].charge_type, CivilOffense)

    assert expunger_result["CASEJD1-1"] == TimeEligibility(
        status=EligibilityStatus.ELIGIBLE,
        reason="Eligible now",
        date_will_be_eligible=mj_charge.disposition.date + relativedelta(years=3),
    )

    assert expunger_result["CASEJD1-2"] == TimeEligibility(
        status=EligibilityStatus.INELIGIBLE,
        reason="Never. Type ineligible charges are always time ineligible.",
        date_will_be_eligible=date.max(),
    )


def test_expunger_for_record_with_mj_under_21_blocked_by_blocking_conviction():
    record = CrawlerFactory.create(
        record=YoungDoe.SINGLE_CASE_RECORD, cases={"CASEJD1": CaseDetails.CASE_MJ_AND_FELONY_CONVICTION}
    )
    expunger_result = Expunger.run(record)

    mj_charge = record.charges[0]
    felony_charge = record.charges[1]

    assert isinstance(mj_charge.charge_type, MarijuanaUnder21)
    assert isinstance(felony_charge.charge_type, FelonyClassA)

    assert expunger_result["CASEJD1-1"] == TimeEligibility(
        status=EligibilityStatus.ELIGIBLE,
        reason="Eligible now",
        date_will_be_eligible=date(1998, 3, 3) + relativedelta(years=3),
    )
    assert expunger_result["CASEJD1-2"] == TimeEligibility(
        status=EligibilityStatus.INELIGIBLE,
        reason="Never. Type ineligible charges are always time ineligible.",
        date_will_be_eligible=date.max(),
    )
