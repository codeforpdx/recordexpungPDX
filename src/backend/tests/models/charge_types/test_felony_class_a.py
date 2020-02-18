from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_felony_class_a_charge():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Assault in the first degree"
    charge_dict["statute"] = "163.185"
    charge_dict["level"] = "Felony Class A"
    charge_dict["disposition"] = Dispositions.CONVICTED
    felony_class_a_convicted = ChargeFactory.create(**charge_dict)

    assert isinstance(felony_class_a_convicted, FelonyClassA)
    assert felony_class_a_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert felony_class_a_convicted.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"


def test_felony_class_a_dismissed():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Assault in the first degree"
    charge_dict["statute"] = "163.185"
    charge_dict["level"] = "Felony Class A"
    charge_dict["disposition"] = Dispositions.DISMISSED
    felony_class_a_dismissed = ChargeFactory.create(**charge_dict)

    assert isinstance(felony_class_a_dismissed, FelonyClassA)
    assert felony_class_a_dismissed.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        felony_class_a_dismissed.expungement_result.type_eligibility.reason
        == "Dismissals are eligible under 137.225(1)(b)"
    )


def test_felony_class_a_no_complaint():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["disposition"] = Dispositions.NO_COMPLAINT
    charge_dict["name"] = "Assault in the first degree"
    charge_dict["statute"] = "163.185"
    charge_dict["level"] = "Felony Class A"
    felony_class_a_no_complaint = ChargeFactory.create(**charge_dict)

    assert isinstance(felony_class_a_no_complaint, FelonyClassA)
    assert felony_class_a_no_complaint.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        felony_class_a_no_complaint.expungement_result.type_eligibility.reason
        == "Dismissals are eligible under 137.225(1)(b)"
    )
