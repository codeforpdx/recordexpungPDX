from expungeservice.models.charge_types.severe_charge import SevereCharge
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_murder_charge():
    murder_convicted = ChargeFactory.create(
        name="Aggravated Murder", statute="163.095", level="Felony Unclassified", disposition=Dispositions.CONVICTED,
    )

    assert isinstance(murder_convicted.charge_type, SevereCharge)
    assert murder_convicted.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert murder_convicted.type_eligibility.reason == "Ineligible by omission from statute"


def test_treason_charge():
    treason_convicted = ChargeFactory.create(
        name="Treason", statute="166.005", level="Felony Unclassified", disposition=Dispositions.CONVICTED,
    )

    assert isinstance(treason_convicted.charge_type, SevereCharge)
    assert treason_convicted.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert treason_convicted.type_eligibility.reason == "Ineligible by omission from statute"
