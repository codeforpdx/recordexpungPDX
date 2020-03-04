from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
import pytest

person_felonies_with_other_charge_type = [
    "475B359",  # Arson Incident to Manufacture of Cannabinoid Extract I;
    "475B367",  # Causing Another Person to Ingest Marijuana;
    "475B371",  # Administration to Another Person Under 18 Years of Age;
    "811705",  # Hit and Run Vehicle (Injury);
    "8130105",  # Felony Driving Under the Influence of Intoxicants (as provided in OAR 213-004-0009);
    "163145",  # [Subsection 6] Negligent Homicide;
    "163165",  # [Subsection 6] Assault III;
    "163205",  # [Subsection 6]  Criminal Mistreatment I;
]


@pytest.mark.parametrize("person_felony_statute", PersonFelonyClassB.statutes)
def test_person_felony_class_b(person_felony_statute):
    person_felony_class_b_convicted = ChargeFactory.create(
        name="Generic", statute=person_felony_statute, level="Felony Class B", disposition=Dispositions.CONVICTED
    )
    assert isinstance(person_felony_class_b_convicted, PersonFelonyClassB)
    assert person_felony_class_b_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        person_felony_class_b_convicted.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)(a)"
    )


@pytest.mark.parametrize("person_felony_statute", PersonFelonyClassB.statutes_with_subsection)
def test_felony_b_person_felony_with_missing_subsection(person_felony_statute):
    person_felony_class_b_convicted = ChargeFactory.create(
        name="Generic", statute=person_felony_statute[:6], level="Felony Class B", disposition=Dispositions.CONVICTED
    )
    assert isinstance(person_felony_class_b_convicted, PersonFelonyClassB)
    assert (
        person_felony_class_b_convicted.expungement_result.type_eligibility.status
        is EligibilityStatus.NEEDS_MORE_ANALYSIS
    )
    assert (
        person_felony_class_b_convicted.expungement_result.type_eligibility.reason
        == "OECI may be missing a statute subsection which would make this charge a person crime, and thus ineligible under 137.225(5)(a)"
    )


@pytest.mark.parametrize("person_felony_statute_with_other_charge_type", person_felonies_with_other_charge_type)
def test_other_charge_type_true_negatives(person_felony_statute_with_other_charge_type):
    person_felony_with_other_charge_type_convicted = ChargeFactory.create(
        name="Generic",
        statute=person_felony_statute_with_other_charge_type,
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )
    assert not isinstance(person_felony_with_other_charge_type_convicted, PersonFelonyClassB)


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
