from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.record_merger import RecordMerger
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
import pytest

person_felonies_with_other_charge_type = [
    "475B359",  # Arson Incident to Manufacture of Cannabinoid Extract I;
    "475B367",  # Causing Another Person to Ingest Marijuana;
    "475B371",  # Administration to Another Person Under 18 Years of Age;
    "811705",  # Hit and Run Vehicle (Injury);
    "8130105",  # Felony Driving Under the Influence of Intoxicants (as provided in OAR 213-004-0009);
]


@pytest.mark.parametrize("person_felony_statute", PersonFelonyClassB.statutes)
def test_person_felony_class_b(person_felony_statute):
    charges = ChargeFactory.create_ambiguous_charge(
        name="Generic", statute=person_felony_statute, level="Felony Class B", disposition=Dispositions.CONVICTED
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)
    assert any([isinstance(charge, PersonFelonyClassB) for charge in charges])
    assert type_eligibility.status in [EligibilityStatus.NEEDS_MORE_ANALYSIS, EligibilityStatus.INELIGIBLE]
    assert "Ineligible under 137.225(5)(a)" in type_eligibility.reason


@pytest.mark.parametrize("person_felony_statute", PersonFelonyClassB.statutes_with_subsection)
def test_felony_b_person_felony_with_missing_subsection(person_felony_statute):
    person_felony_class_b_convicted = ChargeFactory.create(
        name="Generic", statute=person_felony_statute[:6], level="Felony Class B", disposition=Dispositions.CONVICTED
    )
    assert isinstance(person_felony_class_b_convicted, PersonFelonyClassB)
    assert person_felony_class_b_convicted.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert person_felony_class_b_convicted.type_eligibility.reason == "Ineligible under 137.225(5)(a)"


@pytest.mark.parametrize("person_felony_statute_with_other_charge_type", person_felonies_with_other_charge_type)
def test_other_charge_type_true_negatives(person_felony_statute_with_other_charge_type):
    charges = ChargeFactory.create_ambiguous_charge(
        name="Generic",
        statute=person_felony_statute_with_other_charge_type,
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )
    assert [not isinstance(charge, PersonFelonyClassB) for charge in charges]


@pytest.mark.parametrize("person_felony_statute_not_b_felony", PersonFelonyClassB.statutes[:5])
def test_felony_not_b_person_felony(person_felony_statute_not_b_felony):
    """
    Only test the first 5 statutes just to not spam another ~75 tests.
    """
    person_felony_not_class_b_convicted = ChargeFactory.create(
        name="Generic",
        statute=person_felony_statute_not_b_felony,
        level="Felony Class C",
        disposition=Dispositions.CONVICTED,
    )
    assert not isinstance(person_felony_not_class_b_convicted, PersonFelonyClassB)
