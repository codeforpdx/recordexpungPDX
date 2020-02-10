from expungeservice.expunger import Expunger
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.expunger_factory import ExpungerFactory
from tests.time import Time


def test_arrest_is_unaffected_if_conviction_is_older():
    # A single violation doesn't block other records, but it is still subject to the 3 year rule.
    violation_charge = ChargeFactory.create(
        level="Class A Violation", date=Time.TEN_YEARS_AGO, disposition=["Convicted", Time.LESS_THAN_THREE_YEARS_AGO]
    )
    arrest = ChargeFactory.create(disposition=["Dismissed", Time.ONE_YEAR_AGO])

    case = CaseFactory.create()
    case.charges = [violation_charge, arrest]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert arrest.expungement_result.time_eligibility.date_will_be_eligible == None
    assert arrest.expungement_result.time_eligibility.reason == ""


def test_arrest_time_eligibility_is_set_to_older_violation():
    older_violation = ChargeFactory.create(
        level="Class A Violation",
        date=Time.LESS_THAN_THREE_YEARS_AGO,
        disposition=["Convicted", Time.LESS_THAN_THREE_YEARS_AGO],
    )
    newer_violation = ChargeFactory.create(
        level="Class A Violation", date=Time.TWO_YEARS_AGO, disposition=["Convicted", Time.TWO_YEARS_AGO]
    )
    arrest = ChargeFactory.create(disposition=["Dismissed", Time.ONE_YEAR_AGO])

    case = CaseFactory.create()
    case.charges = [older_violation, newer_violation, arrest]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        arrest.expungement_result.time_eligibility.reason
        == "The friendly rule: time eligibility of the arrest matches time eligibility of the conviction."
    )
    assert (
        arrest.expungement_result.time_eligibility.date_will_be_eligible
        == older_violation.disposition.date + Time.THREE_YEARS
    )


def test_3_violations_are_time_restricted():
    violation_charge_1 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.LESS_THAN_THREE_YEARS_AGO,
        disposition=["Convicted", Time.LESS_THAN_THREE_YEARS_AGO],
    )
    violation_charge_2 = ChargeFactory.create(
        level="Class A Violation", date=Time.TWO_YEARS_AGO, disposition=["Convicted", Time.TWO_YEARS_AGO]
    )
    violation_charge_3 = ChargeFactory.create(
        level="Class A Violation", date=Time.ONE_YEAR_AGO, disposition=["Convicted", Time.ONE_YEAR_AGO]
    )
    arrest = ChargeFactory.create(disposition=["Dismissed", Time.ONE_YEAR_AGO])

    case = CaseFactory.create()
    case.charges = [violation_charge_3, violation_charge_2, violation_charge_1, arrest]
    expunger = Expunger(Record([case]))
    expunger.run()

    earliest_date_eligible = min(
        violation_charge_1.expungement_result.time_eligibility.date_will_be_eligible,
        violation_charge_2.expungement_result.time_eligibility.date_will_be_eligible,
        violation_charge_3.expungement_result.time_eligibility.date_will_be_eligible,
    )

    assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        arrest.expungement_result.time_eligibility.reason
        == "The friendly rule: time eligibility of the arrest matches time eligibility of the conviction."
    )
    assert arrest.expungement_result.time_eligibility.date_will_be_eligible == earliest_date_eligible
