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
