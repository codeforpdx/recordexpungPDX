from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_felony_c_conviction():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Theft in the first degree"
    charge_dict["statute"] = "164.055"
    charge_dict["level"] = "Felony Class C"
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, FelonyClassC)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"


def test_felony_c_dismissal():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.DISMISSED)
    charge_dict["name"] = "Theft in the first degree"
    charge_dict["statute"] = "164.055"
    charge_dict["level"] = "Felony Class C"
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, FelonyClassC)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.expungement_result.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"


def test_felony_c_no_disposition():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Theft in the first degree"
    charge_dict["statute"] = "164.055"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = None
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, FelonyClassC)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        charge.expungement_result.type_eligibility.reason
        == "Eligible under 137.225(5)(b) for convictions or under 137.225(1)(b) for dismissals"
    )


def test_felony_c_unrecognized_disposition():
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.UNRECOGNIZED_DISPOSITION)
    charge_dict["name"] = "Theft in the first degree"
    charge_dict["statute"] = "164.055"
    charge_dict["level"] = "Felony Class C"
    charge_dict["disposition"] = None
    charge = ChargeFactory.create(**charge_dict)

    assert isinstance(charge, FelonyClassC)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        charge.expungement_result.type_eligibility.reason
        == "Eligible under 137.225(5)(b) for convictions or under 137.225(1)(b) for dismissals"
    )
