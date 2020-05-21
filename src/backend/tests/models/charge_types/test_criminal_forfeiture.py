from expungeservice.models.charge_types.criminal_forfeiture import CriminalForfeiture
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_criminal_forfeiture():
    charge = ChargeFactory.create(
        name="Criminal Forfeiture", statute="131582", level="N/A", disposition=Dispositions.UNRECOGNIZED_DISPOSITION
    )
    assert isinstance(charge, CriminalForfeiture)
