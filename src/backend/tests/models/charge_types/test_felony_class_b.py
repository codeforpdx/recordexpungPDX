from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaEligible
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_class_b_felony_164057():
    charge = ChargeFactory.create(
        name="Aggravated theft in the first degree",
        statute="164.057",
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(charge.charge_type, FelonyClassB)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Convictions that fulfill the conditions of 137.225(5)(a) are eligible"


def test_class_felony_is_added_to_b_felony_attribute():
    charge = ChargeFactory.create(
        name="Aggravated theft in the first degree", statute="164.057", level="Felony Class B"
    )

    assert isinstance(charge.charge_type, FelonyClassB)


def test_attempt_to_commit_felony_class_a_charge():
    charge = ChargeFactory.create_ambiguous_charge(
        name="Attempt to Commit a Class A Felony",
        statute="161.405(2)(b)",
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )
    assert isinstance(charge[0].charge_type, MarijuanaEligible)
    assert isinstance(charge[1].charge_type, FelonyClassB)
    assert isinstance(charge[2].charge_type, PersonFelonyClassB)
