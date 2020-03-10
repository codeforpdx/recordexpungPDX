from expungeservice.models.expungement_result import *
from expungeservice.models.helpers.record_merger import RecordMerger
from tests.time import Time


def test_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    time_eligibility = TimeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute", date.today())
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, {time_eligibility})

    assert charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
    assert charge_eligibility.label == "Eligible"


def test_will_be_eligible():
    today = date.today()
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    time_eligibility = TimeEligibility(EligibilityStatus.INELIGIBLE, "Ineligible under some statute", today)
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, {time_eligibility})

    assert charge_eligibility.status == ChargeEligibilityStatus.WILL_BE_ELIGIBLE
    assert charge_eligibility.label == f"Eligible {today.strftime('%b %-d, %Y')}"


def test_possibly_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    time_eligibility = TimeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under for some reason", date.today())
    time_eligibility_2 = TimeEligibility(EligibilityStatus.INELIGIBLE, "Ineligible under some statute", date.max)
    charge_eligibility = RecordMerger.compute_charge_eligibility(
        type_eligibility, {time_eligibility, time_eligibility_2}
    )

    assert charge_eligibility.status == ChargeEligibilityStatus.POSSIBLY_ELIGIBILE
    assert charge_eligibility.label == "Possibly Eligible (review)"


def test_possibly_will_be_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    time_eligibility = TimeEligibility(
        EligibilityStatus.INELIGIBLE, "Ineligible for some reason", Time.ONE_YEARS_FROM_NOW
    )
    time_eligibility_2 = TimeEligibility(EligibilityStatus.INELIGIBLE, "Ineligible under some statute", date.max)
    charge_eligibility = RecordMerger.compute_charge_eligibility(
        type_eligibility, {time_eligibility, time_eligibility_2}
    )

    assert charge_eligibility.status == ChargeEligibilityStatus.POSSIBLY_WILL_BE_ELIGIBLE
    assert charge_eligibility.label == f"Possibly Eligible {Time.ONE_YEARS_FROM_NOW.strftime('%b %-d, %Y')} (review)"


def test_ineligible():
    type_eligibility = TypeEligibility(EligibilityStatus.INELIGIBLE, "Ineligible under some statute")
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, set())

    assert charge_eligibility.status == ChargeEligibilityStatus.INELIGIBLE
    assert charge_eligibility.label == "Ineligible"


def test_type_eligible_never_becomes_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    time_eligibility = TimeEligibility(EligibilityStatus.INELIGIBLE, "Never eligible under some statute", date.max)
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, {time_eligibility})

    assert charge_eligibility.status == ChargeEligibilityStatus.INELIGIBLE
    assert charge_eligibility.label == "Ineligible"


def test_type_possibly_eligible_never_becomes_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    time_eligibility = TimeEligibility(EligibilityStatus.INELIGIBLE, "Never eligible under some statute", date.max)
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, {time_eligibility})

    assert charge_eligibility.status == ChargeEligibilityStatus.INELIGIBLE
    assert charge_eligibility.label == "Ineligible"


def test_type_eligible_but_time_eligibility_missing():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, set())

    assert charge_eligibility.status == ChargeEligibilityStatus.UNKNOWN
    assert charge_eligibility.label == "Possibly eligible but time analysis is missing"


def test_possibly_type_eligible_but_time_eligibility_missing():
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    charge_eligibility = RecordMerger.compute_charge_eligibility(type_eligibility, set())

    assert charge_eligibility.status == ChargeEligibilityStatus.UNKNOWN
    assert charge_eligibility.label == "Possibly eligible but time analysis is missing"
