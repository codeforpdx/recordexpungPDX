from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.sex_crimes import SexCrime
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
import pytest


@pytest.mark.parametrize("sex_crimes_statute", SexCrime.statutes)
def test_sex_crimes(sex_crimes_statute):
    sex_crime_convicted = ChargeFactory.create(
        name="Generic", statute=sex_crimes_statute, level="Felony Class B", disposition=Dispositions.CONVICTED
    )
    assert isinstance(sex_crime_convicted, SexCrime)
    assert sex_crime_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert sex_crime_convicted.expungement_result.type_eligibility.reason == "Ineligible under 137.225(6)(a)"


@pytest.mark.parametrize("sex_crimes_statute", SexCrime.romeo_and_juliet_exceptions)
def test_sex_crimes_with_romeo_and_juliet_exception(sex_crimes_statute):
    sex_crime_romeo_juliet_exception_convicted = ChargeFactory.create(
        name="Generic", statute=sex_crimes_statute, level="Misdemeanor Class A", disposition=Dispositions.CONVICTED
    )
    assert isinstance(sex_crime_romeo_juliet_exception_convicted, SexCrime)
    assert (
        sex_crime_romeo_juliet_exception_convicted.expungement_result.type_eligibility.status
        is EligibilityStatus.NEEDS_MORE_ANALYSIS
    )
    assert (
        sex_crime_romeo_juliet_exception_convicted.expungement_result.type_eligibility.reason
        == "Romeo and Juliet exception, needs other eligibility requirements. See 163A.140(1)"
    )
