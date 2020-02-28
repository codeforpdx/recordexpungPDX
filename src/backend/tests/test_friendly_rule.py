from dateutil.relativedelta import relativedelta

from expungeservice.expunger import Expunger
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import EligibilityStatus, ChargeEligibilityStatus
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.time import Time
from datetime import date


def test_eligible_mrc_with_single_arrest():
    three_yr_mrc = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO))

    arrest = ChargeFactory.create(disposition=Disposition(ruling="Dismissed", date=Time.THREE_YEARS_AGO))

    case = CaseFactory.create()
    case.charges = [three_yr_mrc, arrest]
    record = Record([case])
    expunger = Expunger(record)
    expunger.run()

    assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        arrest.expungement_result.time_eligibility.reason
        == 'Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)'
    )
    assert arrest.expungement_result.time_eligibility.date_will_be_eligible == date.today()
    assert arrest.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
    assert arrest.expungement_result.charge_eligibility.label == "Eligible"

    assert three_yr_mrc.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert three_yr_mrc.expungement_result.time_eligibility.reason == ""
    assert three_yr_mrc.expungement_result.time_eligibility.date_will_be_eligible == date.today()
    assert three_yr_mrc.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
    assert three_yr_mrc.expungement_result.charge_eligibility.label == "Eligible"


def test_arrest_is_unaffected_if_conviction_eligibility_is_older():
    violation_charge = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TEN_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
    )
    arrest = ChargeFactory.create(disposition=Disposition(ruling="Dismissed", date=Time.ONE_YEAR_AGO))

    case = CaseFactory.create()
    case.charges = [violation_charge, arrest]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert arrest.expungement_result.time_eligibility.date_will_be_eligible == arrest.date
    assert arrest.expungement_result.time_eligibility.reason == ""


def test_eligible_mrc_with_violation():
    case = CaseFactory.create()

    three_yr_mrc = ChargeFactory.create(
        case=case, disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO)
    )

    arrest = ChargeFactory.create(case=case, disposition=Disposition(ruling="Dismissed", date=Time.THREE_YEARS_AGO))

    violation = ChargeFactory.create(
        level="Violation", case=case, disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO)
    )

    case.charges = [three_yr_mrc, arrest, violation]
    record = Record([case])
    expunger = Expunger(record)

    expunger.run()
    assert three_yr_mrc.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert three_yr_mrc.expungement_result.time_eligibility.reason == ""
    assert three_yr_mrc.expungement_result.time_eligibility.date_will_be_eligible == date.today()

    assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        arrest.expungement_result.time_eligibility.reason
        == 'Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)'
    )
    assert arrest.expungement_result.time_eligibility.date_will_be_eligible == date.today()

    assert violation.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert violation.expungement_result.time_eligibility.date_will_be_eligible == date.today() + relativedelta(years=7)
    assert (
        violation.expungement_result.time_eligibility.reason
        == "Ten years from most recent other conviction (137.225(7)(b))"
    )


def test_needs_more_analysis_mrc_with_single_arrest():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Assault in the third degree"
    charge_dict["statute"] = "163.165"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO)
    three_yr_mrc = ChargeFactory.create(**charge_dict)
    arrest = ChargeFactory.create(disposition=Disposition(ruling="Dismissed", date=Time.THREE_YEARS_AGO))

    case = CaseFactory.create()
    case.charges = [three_yr_mrc, arrest]
    record = Record([case])
    expunger = Expunger(record)
    expunger.run()

    ten_years_from_mrc = three_yr_mrc.disposition.date + Time.TEN_YEARS
    assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert arrest.expungement_result.time_eligibility.reason == "Ten years from most recent conviction (137.225(7)(b))"
    assert arrest.expungement_result.time_eligibility.date_will_be_eligible == date.today()
    assert arrest.expungement_result.time_eligibility.date_eligible_without_friendly_rule == ten_years_from_mrc
    assert arrest.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.WILL_BE_ELIGIBLE
    assert (
        arrest.expungement_result.charge_eligibility.label
        == f"Eligible now or {ten_years_from_mrc.strftime('%b %-d, %Y')} w/o friendly rule (review)"
    )

    assert three_yr_mrc.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert three_yr_mrc.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert three_yr_mrc.expungement_result.time_eligibility.reason == ""
    assert three_yr_mrc.expungement_result.time_eligibility.date_will_be_eligible == date.today()
    assert three_yr_mrc.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.POSSIBLY_ELIGIBILE
    assert three_yr_mrc.expungement_result.charge_eligibility.label == "Possibly Eligible (review)"


def test_very_old_needs_more_analysis_mrc_with_single_arrest():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Assault in the third degree"
    charge_dict["statute"] = "163.165"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = Disposition(ruling="Convicted", date=Time.TWENTY_YEARS_AGO)
    mrc = ChargeFactory.create(**charge_dict)
    arrest = ChargeFactory.create(disposition=Disposition(ruling="Dismissed", date=Time.THREE_YEARS_AGO))

    case = CaseFactory.create()
    case.charges = [mrc, arrest]
    record = Record([case])
    expunger = Expunger(record)
    expunger.run()

    three_years_from_mrc = mrc.disposition.date + Time.THREE_YEARS
    assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert arrest.expungement_result.time_eligibility.date_will_be_eligible == three_years_from_mrc
    assert arrest.expungement_result.time_eligibility.date_eligible_without_friendly_rule == Time.THREE_YEARS_AGO
    assert arrest.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
    assert arrest.expungement_result.charge_eligibility.label == "Eligible"

    assert mrc.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert mrc.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert mrc.expungement_result.time_eligibility.date_will_be_eligible == three_years_from_mrc
    assert mrc.expungement_result.charge_eligibility.status == ChargeEligibilityStatus.POSSIBLY_ELIGIBILE
    assert mrc.expungement_result.charge_eligibility.label == "Possibly Eligible (review)"


def test_arrest_time_eligibility_is_set_to_older_violation():
    older_violation = ChargeFactory.create(
        level="Class A Violation",
        date=Time.LESS_THAN_THREE_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
    )
    newer_violation = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TWO_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.TWO_YEARS_AGO),
    )
    arrest = ChargeFactory.create(disposition=Disposition(ruling="Dismissed", date=Time.ONE_YEAR_AGO))

    case = CaseFactory.create()
    case.charges = [older_violation, newer_violation, arrest]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        arrest.expungement_result.time_eligibility.reason
        == 'Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)'
    )
    assert (
        arrest.expungement_result.time_eligibility.date_will_be_eligible
        == older_violation.disposition.date + Time.THREE_YEARS
    )


def test_3_violations_are_time_restricted():
    violation_charge_1 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.LESS_THAN_THREE_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
    )
    violation_charge_2 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TWO_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.TWO_YEARS_AGO),
    )
    violation_charge_3 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.ONE_YEAR_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.ONE_YEAR_AGO),
    )
    arrest = ChargeFactory.create(disposition=Disposition(ruling="Dismissed", date=Time.ONE_YEAR_AGO))

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
        == 'Time eligibility of the arrest matches conviction on the same case (the "friendly" rule)'
    )
    assert arrest.expungement_result.time_eligibility.date_will_be_eligible == earliest_date_eligible
