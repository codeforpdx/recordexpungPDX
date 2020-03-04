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

def test_manufacture_delivery_missing_disposition():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Manufacture/Delivery"
    charge_dict["statute"] = "4759922b"
    charge_dict["level"] = "Felony Class A"
    charge_dict["disposition"] = None

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)


    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        manufacture_delivery_charge.expungement_result.type_eligibility.reason == "Possibly eligible. See additional legal details."
    )

def test_manufacture_delivery_unrecognized_disposition():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Manufacture/Delivery"
    charge_dict["statute"] = "4759922b"
    charge_dict["level"] = "Felony Class B"
    charge_dict["disposition"] = Dispositions.UNRECOGNIZED_DISPOSITION

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)


    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        manufacture_delivery_charge.expungement_result.type_eligibility.reason == "Possibly eligible. See additional legal details."
    )

def test_manufacture_delivery_manudel():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Manu/Del Cntrld Sub-SC 1"
    charge_dict["statute"] = "4759921B"
    charge_dict["level"] = "Felony Class A"
    charge_dict["disposition"] = Dispositions.CONVICTED

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        manufacture_delivery_charge.expungement_result.type_eligibility.reason == "This may be eligible if it is a charge for marijuana, under 137.226. See additional legal details."
    )

def test_manufacture_delivery_manudel_felony_unclassified():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "Manu/Del Cntrld Sub-SC 1"
    charge_dict["statute"] = "4759921B"
    charge_dict["level"] = "Felony Unclassified"
    charge_dict["disposition"] = Dispositions.CONVICTED

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS

def test_manufacture_delivery_manufacturing_name():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "MANUFACTURING CONTROLLED SUB"
    charge_dict["statute"] = "4759921A"
    charge_dict["level"] = "Felony Unclassified"
    charge_dict["disposition"] = Dispositions.CONVICTED

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS

def test_manufacture_delivery_1():
    charge_dict = ChargeFactory.default_dict()
    charge_dict["name"] = "MANUFACTURING CONTROLLED SUB 2"
    charge_dict["statute"] = "4759921A"
    charge_dict["level"] = "Felony Unclassified"
    charge_dict["disposition"] = Dispositions.CONVICTED

    manufacture_delivery_charge = ChargeFactory.create(**charge_dict)

    assert not isinstance(manufacture_delivery_charge, ManufactureDelivery)
