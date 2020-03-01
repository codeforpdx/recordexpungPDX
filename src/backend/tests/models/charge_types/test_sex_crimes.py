from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.sex_crimes import SexCrimes
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
import pytest


@pytest.mark.parametrize("sex_crimes_statute", SexCrimes.statutes)
def test_sex_crimes(sex_crimes_statute):
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Generic"
    charge_dict["statute"] = sex_crimes_statute
    charge_dict["level"] = "Felony Class B"
    charge_dict["disposition"] = Dispositions.CONVICTED
    person_felony_class_b_convicted = ChargeFactory.create(**charge_dict)
    assert isinstance(person_felony_class_b_convicted, SexCrimes)
    assert person_felony_class_b_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        person_felony_class_b_convicted.expungement_result.type_eligibility.reason == "Ineligible under 137.225(6)(a)"
    )


@pytest.mark.parametrize("sex_crimes_statute", SexCrimes.romeo_and_juliet_exceptions)
def test_sex_crimes_with_romeo_and_juliet_exception(sex_crimes_statute):
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Generic"
    charge_dict["statute"] = sex_crimes_statute
    charge_dict["level"] = "Misdemeanor Class A"
    charge_dict["disposition"] = Dispositions.CONVICTED
    sex_crime_romeo_juliet_exception_convicted = ChargeFactory.create(**charge_dict)
    assert isinstance(sex_crime_romeo_juliet_exception_convicted, SexCrimes)
    assert (
        sex_crime_romeo_juliet_exception_convicted.expungement_result.type_eligibility.status
        is EligibilityStatus.NEEDS_MORE_ANALYSIS
    )
    assert (
        sex_crime_romeo_juliet_exception_convicted.expungement_result.type_eligibility.reason
        == "Romeo and Juliet exception, needs other elligibility requirements. See 163A.140(1)"
    )
