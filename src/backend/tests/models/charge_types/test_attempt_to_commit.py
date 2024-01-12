from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.sex_crimes import SexCrime
from expungeservice.models.charge_types.traffic_offense import TrafficOffense
from expungeservice.models.charge_types.misdemeanor_class_bc import MisdemeanorClassBC
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaEligible
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.models.charge_types.felony_class_b import FelonyClassB

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_attempt_to_commit_felony_class_b_charge():
    charge = ChargeFactory.create_ambiguous_charge(
        name="Attempt to Commit a Class B Felony",
        statute="161.405(2)(c)",
        level="Felony Class C",
        disposition=Dispositions.CONVICTED,
    )
    assert isinstance(charge[0].charge_type, SexCrime)
    assert isinstance(charge[1].charge_type, TrafficOffense)
    assert isinstance(charge[2].charge_type, FelonyClassC)

def test_attempt_to_commit_a_drug_crime():
    charge = ChargeFactory.create_ambiguous_charge(
        name="Attempt to Commit a Class A Felony",
        statute="161.405(2)(c)",
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )
    assert isinstance(charge[0].charge_type, MarijuanaEligible)
    assert isinstance(charge[1].charge_type, FelonyClassB)
    assert isinstance(charge[2].charge_type, PersonFelonyClassB)
    assert isinstance(charge[3].charge_type, TrafficOffense)

def test_attempt_to_commit_a_low_level_offense():
    charge = ChargeFactory.create_ambiguous_charge(
        name="Attempt to Commit a Class A Misdemeanor",
        statute="161.405(2)(c)",
        level="Misdemeanor Class B",
        disposition=Dispositions.CONVICTED,
    )
    assert len(charge) == 2
    assert isinstance(charge[0].charge_type, TrafficOffense)
    assert isinstance(charge[1].charge_type, MisdemeanorClassBC)
