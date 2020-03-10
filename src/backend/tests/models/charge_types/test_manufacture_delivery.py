from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.manufacture_delivery import ManufactureDelivery
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
import pytest


def test_manufacture_delivery_dismissed():
    manufacture_delivery_charge = ChargeFactory.create(
        name="Manufacture/Delivery", statute="4759922b", level="Felony Class A", disposition=Dispositions.DISMISSED
    )

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert manufacture_delivery_charge.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"


def test_manufacture_delivery_missing_disposition():
    manufacture_delivery_charge = ChargeFactory.create(
        name="Manufacture/Delivery", statute="4759922b", level="Felony Class A", disposition=None
    )

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert manufacture_delivery_charge.type_eligibility.reason == "Possibly eligible. See additional legal details."


def test_manufacture_delivery_unrecognized_disposition():
    manufacture_delivery_charge = ChargeFactory.create(
        name="Manufacture/Delivery",
        statute="4759922b",
        level="Felony Class B",
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
    )

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert manufacture_delivery_charge.type_eligibility.reason == "Possibly eligible. See additional legal details."


def test_manufacture_delivery_manudel():
    manufacture_delivery_charge = ChargeFactory.create(
        name="Manu/Del Cntrld Sub-SC 1", statute="4759921B", level="Felony Class A", disposition=Dispositions.CONVICTED
    )

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        manufacture_delivery_charge.type_eligibility.reason
        == "This may be eligible if it is a charge for marijuana, under 137.226. See additional legal details."
    )


def test_manufacture_delivery_manudel_felony_unclassified():
    manufacture_delivery_charge = ChargeFactory.create(
        name="Manu/Del Cntrld Sub-SC 1",
        statute="4759921B",
        level="Felony Unclassified",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS


def test_manufacture_delivery_manufacturing_name():
    manufacture_delivery_charge = ChargeFactory.create(
        name="MANUFACTURING CONTROLLED SUB",
        statute="4759921A",
        level="Felony Unclassified",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(manufacture_delivery_charge, ManufactureDelivery)
    assert manufacture_delivery_charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS


def test_manufacture_delivery_1():
    manufacture_delivery_charge = ChargeFactory.create(
        name="MANUFACTURING CONTROLLED SUB 2",
        statute="4759921A",
        level="Felony Unclassified",
        disposition=Dispositions.CONVICTED,
    )

    assert not isinstance(manufacture_delivery_charge, ManufactureDelivery)
