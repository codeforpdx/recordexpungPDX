from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaEligible
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
import pytest

delivery_to_minor_charge_dict = ChargeFactory.default_dict()
delivery_to_minor_charge_dict["name"] = "Delivery of Marijuana to Minor"
delivery_to_minor_charge_dict["statute"] = "4758604A"
delivery_to_minor_charge_dict["level"] = "Felony Class A"

def test_delivery_to_minor_4758604A():
    delivery_to_minor_charge_dict["disposition"] = Dispositions.DISMISSED

    marijuana_eligible_charge = ChargeFactory.create(**delivery_to_minor_charge_dict)

    assert isinstance(marijuana_eligible_charge, MarijuanaEligible)
    assert marijuana_eligible_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        marijuana_eligible_charge.expungement_result.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"
    )

def test_marijuana_eligible_convicted():
    delivery_to_minor_charge_dict["disposition"] = Dispositions.CONVICTED

    marijuana_eligible_charge = ChargeFactory.create(**delivery_to_minor_charge_dict)

    assert isinstance(marijuana_eligible_charge, MarijuanaEligible)
    assert marijuana_eligible_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        marijuana_eligible_charge.expungement_result.type_eligibility.reason == "Eligible under 137.226"
    )

def test_marijuana_eligible_missing_dispo():
    delivery_to_minor_charge_dict["disposition"] = None

    marijuana_eligible_charge = ChargeFactory.create(**delivery_to_minor_charge_dict)

    assert isinstance(marijuana_eligible_charge, MarijuanaEligible)
    assert marijuana_eligible_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        marijuana_eligible_charge.expungement_result.type_eligibility.reason == "Always eligible under 137.226 (for convictions) or 137.225(1)(b) (for dismissals)"
    )

def test_marijuana_eligible_missing_dispo():
    delivery_to_minor_charge_dict["disposition"] = Dispositions.UNRECOGNIZED_DISPOSITION

    marijuana_eligible_charge = ChargeFactory.create(**delivery_to_minor_charge_dict)

    assert isinstance(marijuana_eligible_charge, MarijuanaEligible)
    assert marijuana_eligible_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        marijuana_eligible_charge.expungement_result.type_eligibility.reason == "Always eligible under 137.226 (for convictions) or 137.225(1)(b) (for dismissals)"
    )

def test_delivery_4758602():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Delivery of Marijuana for Consideration"
    charge_dict["statute"] = "4758602"
    charge_dict["level"] = "Felony Class B"
    charge_dict["disposition"] = Dispositions.CONVICTED

    marijuana_eligible_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(marijuana_eligible_charge, MarijuanaEligible)
