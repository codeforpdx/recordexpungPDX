from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.manufacture_delivery import ManufactureDelivery
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
import pytest

def test_manufacture_delivery_dismissed():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Manufacture/Delivery"
    charge_dict["statute"] = "4759922b"
    charge_dict["level"] = "Felony Class A"
    charge_dict["disposition"] = Dispositions.DISMISSED

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)


    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        manufacture_delivery_charge.expungement_result.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"
    )

def test_manufacture_delivery_manudel():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Manu/Del Cntrld Sub-SC 2"
    charge_dict["statute"] = "4759921B"
    charge_dict["level"] = "Felony Class A"
    charge_dict["disposition"] = Dispositions.CONVICTED

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        manufacture_delivery_charge.expungement_result.type_eligibility.reason == "If this is a marijuana conviction, it's eligible under 137.226. Otherwise it's ineligible by omission from statute."
    )

def test_manufacture_delivery_manudel_felony_unclassified():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Manu/Del Cntrld Sub-SC 2"
    charge_dict["statute"] = "4759921B"
    charge_dict["level"] = "Felony Unclassified"
    charge_dict["disposition"] = Dispositions.CONVICTED

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        manufacture_delivery_charge.expungement_result.type_eligibility.reason == "Possibly eligible under 137.225(5)(a), if this is a Class B Felony. If so, time eligibility follows the 20-year B felony rule."
    )

@pytest.mark.skip(reason="We don't look for 'manufactur' keyword which picks up false positives. But we need to classify this as Manu/Del")
def test_manufacture_delivery_manufacturing_name_4759921a():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "MANUFACTURING CONTROLLED SUB"
    charge_dict["statute"] = "4759921A"
    charge_dict["level"] = "Felony Unclassified"
    charge_dict["disposition"] = Dispositions.CONVICTED

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        manufacture_delivery_charge.expungement_result.type_eligibility.reason == "Possibly eligible under 137.225(5)(a), if this is a Class B Felony. If so, time eligibility follows the 20-year B felony rule."
    )

@pytest.mark.skip(reason="WIP")
def test_manufacture_delivery_475860():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Delivery of Marijuana for Consideration"
    charge_dict["statute"] = "4758602"
    charge_dict["level"] = "Felony Class B"
    charge_dict["disposition"] = Dispositions.CONVICTED

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        manufacture_delivery_charge.expungement_result.type_eligibility.reason == "Possibly eligible under 137.225(5)(a), if this is a Class B Felony. If so, time eligibility follows the 20-year B felony rule."
    )
