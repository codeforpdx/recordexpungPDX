from expungeservice.models.charge_types.dismissed_charge import DismissedCharge
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.disposition import DispositionCreator
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_felony_c_conviction():
    charge = ChargeFactory.create(
        name="Theft in the first degree", statute="164.055", level="Felony Class C", disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge.charge_type, FelonyClassC)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Eligible under 137.225(1)(b)"


def test_felony_c_dismissal():
    charge = ChargeFactory.create(
        name="Theft in the first degree", statute="164.055", level="Felony Class C", disposition=Dispositions.DISMISSED
    )

    assert isinstance(charge.charge_type, DismissedCharge)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.type_eligibility.reason == "Dismissals are generally eligible under 137.225(1)(d)"


def test_felony_c_no_disposition():
    charge = ChargeFactory.create(
        name="Theft in the first degree",
        statute="164.055",
        level="Felony Class C",
        disposition=DispositionCreator.empty(),
    )

    assert isinstance(charge.charge_type, FelonyClassC)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        charge.type_eligibility.reason
        == "Eligible under 137.225(1)(b) for convictions or under 137.225(1)(d) for dismissals"
    )


def test_felony_c_unrecognized_disposition():
    charge = ChargeFactory.create(
        name="Theft in the first degree",
        statute="164.055",
        level="Felony Class C",
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
    )

    assert isinstance(charge.charge_type, FelonyClassC)
    assert charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        charge.type_eligibility.reason
        == "Eligible under 137.225(1)(b) for convictions or under 137.225(1)(d) for dismissals"
    )
