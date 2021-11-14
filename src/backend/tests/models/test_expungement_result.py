from expungeservice.models.expungement_result import (
    TypeEligibility,
    EligibilityStatus,
    TimeEligibility,
    ChargeEligibilityStatus,
)
from expungeservice.record_merger import RecordMerger
from tests.time import Time
from expungeservice.util import DateWithFuture as date


def test_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    time_eligibility = TimeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute", date.today())
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, [time_eligibility])

    assert charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
    assert charge_eligibility.label == "Eligible Now"


def test_will_be_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    time_eligibility = TimeEligibility(
        EligibilityStatus.INELIGIBLE, "Ineligible under some statute", Time.ONE_YEARS_FROM_NOW
    )
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, [time_eligibility])

    assert charge_eligibility.status == ChargeEligibilityStatus.WILL_BE_ELIGIBLE
    assert charge_eligibility.label == f"Eligible {Time.ONE_YEARS_FROM_NOW.strftime('%b %-d, %Y')}"


def test_possibly_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    time_eligibility = TimeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under for some reason", date.today())
    time_eligibility_2 = TimeEligibility(EligibilityStatus.INELIGIBLE, "Ineligible under some statute", date.max())
    charge_eligibility = RecordMerger.compute_charge_eligibility(
        type_eligibility, [time_eligibility, time_eligibility_2]
    )

    assert charge_eligibility.status == ChargeEligibilityStatus.POSSIBLY_ELIGIBILE
    assert charge_eligibility.label == "Possibly Eligible Now"


def test_possibly_will_be_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    time_eligibility = TimeEligibility(
        EligibilityStatus.INELIGIBLE, "Ineligible for some reason", Time.ONE_YEARS_FROM_NOW
    )
    time_eligibility_2 = TimeEligibility(EligibilityStatus.INELIGIBLE, "Ineligible under some statute", date.max())
    charge_eligibility = RecordMerger.compute_charge_eligibility(
        type_eligibility, [time_eligibility, time_eligibility_2]
    )

    assert charge_eligibility.status == ChargeEligibilityStatus.POSSIBLY_WILL_BE_ELIGIBLE
    assert charge_eligibility.label == f"Possibly Eligible {Time.ONE_YEARS_FROM_NOW.strftime('%b %-d, %Y')}"


def test_multiple_will_be_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    time_eligibility = TimeEligibility(EligibilityStatus.ELIGIBLE, "Eligible Now", Time.THREE_YEARS_AGO)
    time_eligibility_2 = TimeEligibility(
        EligibilityStatus.INELIGIBLE, "Ineligible under some statute", Time.ONE_YEARS_FROM_NOW
    )
    charge_eligibility = RecordMerger.compute_charge_eligibility(
        type_eligibility, [time_eligibility, time_eligibility_2]
    )

    assert charge_eligibility.status == ChargeEligibilityStatus.WILL_BE_ELIGIBLE
    assert charge_eligibility.label == f"Eligible Now or {Time.ONE_YEARS_FROM_NOW.strftime('%b %-d, %Y')}"


def test_ineligible():
    type_eligibility = TypeEligibility(EligibilityStatus.INELIGIBLE, "Ineligible under some statute")
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, [])

    assert charge_eligibility.status == ChargeEligibilityStatus.INELIGIBLE
    assert charge_eligibility.label == "Ineligible"


def test_type_eligible_never_becomes_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    time_eligibility = TimeEligibility(EligibilityStatus.INELIGIBLE, "Never eligible under some statute", date.max())
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, [time_eligibility])

    assert charge_eligibility.status == ChargeEligibilityStatus.INELIGIBLE
    assert charge_eligibility.label == "Ineligible"


def test_type_possibly_eligible_never_becomes_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    time_eligibility = TimeEligibility(EligibilityStatus.INELIGIBLE, "Never eligible under some statute", date.max())
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, [time_eligibility])

    assert charge_eligibility.status == ChargeEligibilityStatus.INELIGIBLE
    assert charge_eligibility.label == "Ineligible"


def test_type_eligible_but_time_eligibility_missing():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, [])

    assert charge_eligibility.status == ChargeEligibilityStatus.UNKNOWN
    assert charge_eligibility.label == "Possibly Eligible"


def test_possibly_type_eligible_but_time_eligibility_missing():
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, [])

    assert charge_eligibility.status == ChargeEligibilityStatus.UNKNOWN
    assert charge_eligibility.label == "Possibly Eligible"
