from expungeservice.models.charge_types.dismissed_charge import DismissedCharge
from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_felony_class_a_charge():
    felony_class_a_convicted = ChargeFactory.create(
        name="Assault in the first degree",
        statute="163.185",
        level="Felony Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(felony_class_a_convicted.charge_type, FelonyClassA)
    assert felony_class_a_convicted.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert felony_class_a_convicted.type_eligibility.reason == "Ineligible by omission from statute"


def test_felony_class_a_dismissed():
    felony_class_a_dismissed = ChargeFactory.create(
        name="Assault in the first degree",
        statute="163.185",
        level="Felony Class A",
        disposition=Dispositions.DISMISSED,
    )

    assert isinstance(felony_class_a_dismissed.charge_type, DismissedCharge)
    assert felony_class_a_dismissed.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert felony_class_a_dismissed.type_eligibility.reason == "Dismissals are generally eligible under 137.225(1)(b)"


def test_felony_class_a_no_complaint():
    felony_class_a_no_complaint = ChargeFactory.create(
        name="Assault in the first degree",
        statute="163.185",
        level="Felony Class A",
        disposition=Dispositions.NO_COMPLAINT,
    )

    assert isinstance(felony_class_a_no_complaint.charge_type, DismissedCharge)
    assert felony_class_a_no_complaint.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        felony_class_a_no_complaint.type_eligibility.reason == "Dismissals are generally eligible under 137.225(1)(b)"
    )
