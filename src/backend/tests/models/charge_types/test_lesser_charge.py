from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.sex_crimes import SexCrime
from expungeservice.models.charge_types.traffic_offense import TrafficOffense
from expungeservice.models.charge_types.misdemeanor_class_bc import MisdemeanorClassBC
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaEligible
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.lesser_charge import LesserChargeEligible, LesserChargeIneligible

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_lesser_charge():
    charge = ChargeFactory.create_ambiguous_charge(
        name="Manufacture/Delivery", 
        statute="4759922b", 
        level="Felony Class A",
        disposition=Dispositions.LESSER_CHARGE,
    )
    assert isinstance(charge[0].charge_type, LesserChargeEligible)
    assert isinstance(charge[1].charge_type, LesserChargeIneligible)
