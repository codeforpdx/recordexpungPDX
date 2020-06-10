from dateutil.relativedelta import relativedelta

from expungeservice.expunger import Expunger
from expungeservice.models.disposition import DispositionCreator
from expungeservice.models.expungement_result import EligibilityStatus, ChargeEligibilityStatus
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.time import Time
from expungeservice.util import DateWithFuture as date


def test_eligible_mrc_with_single_arrest():
    three_yr_mrc = ChargeFactory.create(
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.THREE_YEARS_AGO)
    )

    arrest = ChargeFactory.create(disposition=DispositionCreator.create(ruling="Dismissed", date=Time.THREE_YEARS_AGO))

    case = CaseFactory.create(charges=tuple([three_yr_mrc, arrest]))
    record = Record(tuple([case]))
    expunger_result = Expunger.run(record)

    assert expunger_result[arrest.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert (
        expunger_result[arrest.ambiguous_charge_id].reason
        == 'Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)'
    )
    assert expunger_result[arrest.ambiguous_charge_id].date_will_be_eligible == date.today()

    assert expunger_result[three_yr_mrc.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[three_yr_mrc.ambiguous_charge_id].reason == "Eligible now"
    assert expunger_result[three_yr_mrc.ambiguous_charge_id].date_will_be_eligible == date.today()

    merged_record = RecordMerger.merge([record], [expunger_result], [])
    assert (
        merged_record.cases[0].charges[0].expungement_result.charge_eligibility.status  # type: ignore
        == ChargeEligibilityStatus.ELIGIBLE_NOW
    )
    assert merged_record.cases[0].charges[0].expungement_result.charge_eligibility.label == "Eligible Now"  # type: ignore

    assert (
        merged_record.cases[0].charges[1].expungement_result.charge_eligibility.status  # type: ignore
        == ChargeEligibilityStatus.ELIGIBLE_NOW
    )
    assert merged_record.cases[0].charges[1].expungement_result.charge_eligibility.label == "Eligible Now"  # type: ignore


def test_arrest_is_unaffected_if_conviction_eligibility_is_older():
    violation_charge = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TEN_YEARS_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
    )
    arrest = ChargeFactory.create(disposition=DispositionCreator.create(ruling="Dismissed", date=Time.ONE_YEAR_AGO))

    case = CaseFactory.create(charges=tuple([violation_charge, arrest]))
    expunger_result = Expunger.run(Record(tuple([case])))

    assert expunger_result[arrest.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[arrest.ambiguous_charge_id].date_will_be_eligible == arrest.date
    assert expunger_result[arrest.ambiguous_charge_id].reason == "Eligible now"


def test_eligible_mrc_with_violation():

    three_yr_mrc = ChargeFactory.create(
        case_number="1", disposition=DispositionCreator.create(ruling="Convicted", date=Time.THREE_YEARS_AGO),
    )

    arrest = ChargeFactory.create(
        case_number="1", disposition=DispositionCreator.create(ruling="Dismissed", date=Time.THREE_YEARS_AGO),
    )

    violation = ChargeFactory.create(
        level="Violation",
        case_number="1",
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.THREE_YEARS_AGO),
    )
    case = CaseFactory.create(case_number="1", charges=tuple([three_yr_mrc, arrest, violation]))
    record = Record(tuple([case]))
    expunger_result = Expunger.run(record)

    assert expunger_result[three_yr_mrc.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[three_yr_mrc.ambiguous_charge_id].reason == "Eligible now"
    assert expunger_result[three_yr_mrc.ambiguous_charge_id].date_will_be_eligible == date.today()

    assert expunger_result[arrest.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert (
        expunger_result[arrest.ambiguous_charge_id].reason
        == 'Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)'
    )
    assert expunger_result[arrest.ambiguous_charge_id].date_will_be_eligible == date.today()

    assert expunger_result[violation.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert expunger_result[violation.ambiguous_charge_id].date_will_be_eligible == date.today() + relativedelta(years=7)
    assert (
        expunger_result[violation.ambiguous_charge_id].reason
        == "Ten years from most recent other conviction (137.225(7)(b))"
    )


def test_needs_more_analysis_mrc_with_single_arrest():
    eligible_charge, ineligible_charge = ChargeFactory.create_ambiguous_charge(
        name="Assault in the third degree",
        statute="163.165",
        level="Felony Class C",
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.THREE_YEARS_AGO),
    )
    arrest = ChargeFactory.create(disposition=DispositionCreator.create(ruling="Dismissed", date=Time.THREE_YEARS_AGO))

    case_a = CaseFactory.create(charges=tuple([eligible_charge, arrest]))
    case_b = CaseFactory.create(charges=tuple([ineligible_charge, arrest]))
    record_a = Record(tuple([case_a]))
    record_b = Record(tuple([case_b]))
    expunger_result_a = Expunger.run(record_a)
    expunger_result_b = Expunger.run(record_b)

    ten_years_from_mrc = eligible_charge.disposition.date + Time.TEN_YEARS
    assert expunger_result_a[arrest.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert (
        expunger_result_a[arrest.ambiguous_charge_id].reason
        == 'Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)'
    )
    assert expunger_result_a[arrest.ambiguous_charge_id].date_will_be_eligible == date.today()

    assert expunger_result_b[arrest.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result_b[arrest.ambiguous_charge_id].reason == "Ten years from most recent conviction (137.225(7)(b))"
    )
    assert expunger_result_b[arrest.ambiguous_charge_id].date_will_be_eligible == ten_years_from_mrc


def test_very_old_needs_more_analysis_mrc_with_single_arrest():
    eligible_charge, ineligible_charge = ChargeFactory.create_ambiguous_charge(
        name="Assault in the third degree",
        statute="163.165",
        level="Felony Class C",
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.TWENTY_YEARS_AGO),
    )
    arrest = ChargeFactory.create(disposition=DispositionCreator.create(ruling="Dismissed", date=Time.THREE_YEARS_AGO))

    case_a = CaseFactory.create(charges=tuple([eligible_charge, arrest]))
    case_b = CaseFactory.create(charges=tuple([ineligible_charge, arrest]))
    record_a = Record(tuple([case_a]))
    record_b = Record(tuple([case_b]))
    expunger_result_a = Expunger.run(record_a)
    expunger_result_b = Expunger.run(record_b)

    three_years_from_mrc = eligible_charge.disposition.date + Time.THREE_YEARS
    assert expunger_result_a[arrest.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert (
        expunger_result_a[arrest.ambiguous_charge_id].reason
        == 'Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)'
    )
    assert expunger_result_a[arrest.ambiguous_charge_id].date_will_be_eligible == three_years_from_mrc

    assert expunger_result_b[arrest.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result_b[arrest.ambiguous_charge_id].reason == "Eligible now"
    assert expunger_result_b[arrest.ambiguous_charge_id].date_will_be_eligible == arrest.disposition.date


def test_arrest_time_eligibility_is_set_to_older_violation():
    older_violation = ChargeFactory.create(
        level="Class A Violation",
        date=Time.LESS_THAN_THREE_YEARS_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
    )
    newer_violation = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TWO_YEARS_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.TWO_YEARS_AGO),
    )
    arrest = ChargeFactory.create(disposition=DispositionCreator.create(ruling="Dismissed", date=Time.ONE_YEAR_AGO))

    case = CaseFactory.create(charges=tuple([older_violation, newer_violation, arrest]))
    expunger_result = Expunger.run(Record(tuple([case])))

    assert expunger_result[arrest.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[arrest.ambiguous_charge_id].reason
        == 'Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)'
    )
    assert (
        expunger_result[arrest.ambiguous_charge_id].date_will_be_eligible
        == older_violation.disposition.date + Time.THREE_YEARS
    )


def test_3_violations_are_time_restricted():
    violation_charge_1 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.LESS_THAN_THREE_YEARS_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
    )
    violation_charge_2 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TWO_YEARS_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.TWO_YEARS_AGO),
    )
    violation_charge_3 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.ONE_YEAR_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.ONE_YEAR_AGO),
    )
    arrest = ChargeFactory.create(disposition=DispositionCreator.create(ruling="Dismissed", date=Time.ONE_YEAR_AGO))

    case = CaseFactory.create(charges=tuple([violation_charge_3, violation_charge_2, violation_charge_1, arrest]))
    expunger_result = Expunger.run(Record(tuple([case])))

    earliest_date_eligible = min(
        expunger_result[violation_charge_1.ambiguous_charge_id].date_will_be_eligible,
        expunger_result[violation_charge_2.ambiguous_charge_id].date_will_be_eligible,
        expunger_result[violation_charge_3.ambiguous_charge_id].date_will_be_eligible,
    )

    assert expunger_result[arrest.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[arrest.ambiguous_charge_id].reason
        == 'Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)'
    )
    assert expunger_result[arrest.ambiguous_charge_id].date_will_be_eligible == earliest_date_eligible
