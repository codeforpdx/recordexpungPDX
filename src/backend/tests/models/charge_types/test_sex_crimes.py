from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.sex_crimes import SexCrime, RomeoAndJulietIneligibleSexCrime
from expungeservice.models.helpers.record_merger import RecordMerger
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
import pytest


@pytest.mark.parametrize("sex_crimes_statute", SexCrime.statutes)
def test_sex_crimes(sex_crimes_statute):
    sex_crime_convicted = ChargeFactory.create(
        name="Generic", statute=sex_crimes_statute, level="Felony Class B", disposition=Dispositions.CONVICTED
    )
    assert isinstance(sex_crime_convicted, SexCrime)
    assert sex_crime_convicted.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert sex_crime_convicted.type_eligibility.reason == "Ineligible under 137.225(6)(a)"


@pytest.mark.parametrize("sex_crimes_statute", SexCrime.romeo_and_juliet_exceptions)
def test_sex_crimes_with_romeo_and_juliet_exception(sex_crimes_statute):
    charges = ChargeFactory.create_ambiguous_charge(
        name="Generic", statute=sex_crimes_statute, level="Misdemeanor Class A", disposition=Dispositions.CONVICTED
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)
    assert isinstance(charges[0], RomeoAndJulietIneligibleSexCrime)
    assert isinstance(charges[1], Misdemeanor)
    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert type_eligibility.reason == "Eligible under 137.225(5)(b), Failure to meet requirements under 163A.140(1)"
