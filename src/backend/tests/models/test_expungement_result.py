from expungeservice.models.expungement_result import *


def test_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    time_eligibility = TimeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute", None)
    expungement_result = ExpungementResult(type_eligibility, time_eligibility)

    assert expungement_result.charge_eligibility.status == ChargeEligibilityStatus.ELIGIBLE_NOW
    assert expungement_result.charge_eligibility.label == "Eligible"
    assert expungement_result.charge_eligibility.date_will_be_eligible is None


def test_will_be_eligible():
    today = date.today()
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    time_eligibility = TimeEligibility(EligibilityStatus.INELIGIBLE, "Ineligible under some statute", today)
    expungement_result = ExpungementResult(type_eligibility, time_eligibility)

    assert expungement_result.charge_eligibility.status == ChargeEligibilityStatus.WILL_BE_ELIGIBLE
    assert expungement_result.charge_eligibility.label == f"Eligible {today.strftime('%b %-d, %Y')}"
    assert expungement_result.charge_eligibility.date_will_be_eligible == today


def test_possibly_eligible():
    today = date.today()
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    time_eligibility = TimeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute", None)
    expungement_result = ExpungementResult(type_eligibility, time_eligibility)

    assert expungement_result.charge_eligibility.status == ChargeEligibilityStatus.POSSIBLY_ELIGIBILE
    assert expungement_result.charge_eligibility.label == "Possibly Eligible (review)"
    assert expungement_result.charge_eligibility.date_will_be_eligible is None


def test_possibly_will_be_eligible():
    today = date.today()
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    time_eligibility = TimeEligibility(EligibilityStatus.INELIGIBLE, "Ineligible under some statute", today)
    expungement_result = ExpungementResult(type_eligibility, time_eligibility)

    assert expungement_result.charge_eligibility.status == ChargeEligibilityStatus.POSSIBLY_WILL_BE_ELIGIBLE
    assert expungement_result.charge_eligibility.label == f"Possibly Eligible {today.strftime('%b %-d, %Y')} (review)"
    assert expungement_result.charge_eligibility.date_will_be_eligible == today


def test_ineligible():
    type_eligibility = TypeEligibility(EligibilityStatus.INELIGIBLE, "Ineligible under some statute")
    expungement_result = ExpungementResult(type_eligibility, None)

    assert expungement_result.charge_eligibility.status == ChargeEligibilityStatus.INELIGIBLE
    assert expungement_result.charge_eligibility.label == "Ineligible"


def test_type_eligible_never_becomes_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    time_eligibility = TimeEligibility(EligibilityStatus.INELIGIBLE, "Never eligible under some statute", date.max)
    expungement_result = ExpungementResult(type_eligibility, time_eligibility)

    assert expungement_result.charge_eligibility.status == ChargeEligibilityStatus.INELIGIBLE
    assert expungement_result.charge_eligibility.label == "Ineligible"


def test_type_possibly_eligible_never_becomes_eligible():
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    time_eligibility = TimeEligibility(EligibilityStatus.INELIGIBLE, "Never eligible under some statute", date.max)
    expungement_result = ExpungementResult(type_eligibility, time_eligibility)

    assert expungement_result.charge_eligibility.status == ChargeEligibilityStatus.INELIGIBLE
    assert expungement_result.charge_eligibility.label == "Ineligible"


def test_type_eligible_but_time_eligibility_missing():
    type_eligibility = TypeEligibility(EligibilityStatus.ELIGIBLE, "Eligible under some statute")
    expungement_result = ExpungementResult(type_eligibility, None)

    assert expungement_result.charge_eligibility.status == ChargeEligibilityStatus.UNKNOWN
    assert expungement_result.charge_eligibility.label == "Type-eligible but time analysis is missing"


def test_possibly_type_eligible_but_time_eligibility_missing():
    type_eligibility = TypeEligibility(EligibilityStatus.NEEDS_MORE_ANALYSIS, "Unrecognized charge")
    expungement_result = ExpungementResult(type_eligibility, None)

    assert expungement_result.charge_eligibility.status == ChargeEligibilityStatus.UNKNOWN
    assert expungement_result.charge_eligibility.label == "Possibly eligible but time analysis is missing"
