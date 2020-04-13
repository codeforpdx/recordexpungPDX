from expungeservice.models.charge_types.civil_offense import CivilOffense

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_00_is_not_a_civil_offense():
    charge = ChargeFactory.create(statute="00", level="N/A", disposition=Dispositions.CONVICTED)

    assert not isinstance(charge, CivilOffense)


def test_100_is_not_a_civil_offense():
    charge = ChargeFactory.create(statute="100", level="N/A", disposition=Dispositions.CONVICTED)

    assert not isinstance(charge, CivilOffense)


def test_99_is_a_civil_offense():
    charge = ChargeFactory.create(statute="99", level="N/A", disposition=Dispositions.CONVICTED)

    assert isinstance(charge, CivilOffense)


def test_55_is_a_civil_offense():
    charge = ChargeFactory.create(statute="55", level="N/A", disposition=Dispositions.CONVICTED)

    assert isinstance(charge, CivilOffense)


def test_2915_is_a_civil_offense():
    charge = ChargeFactory.create(statute="2915", level="N/A", disposition=Dispositions.CONVICTED)
    assert isinstance(charge, CivilOffense)


def test_fugitive_complaint():
    charge = ChargeFactory.create(
        statute="0", level="N/A", name="Fugitive Complaint", disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, CivilOffense)
