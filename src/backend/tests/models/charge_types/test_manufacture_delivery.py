from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.record_merger import RecordMerger
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_manufacture_delivery_dismissed():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Manufacture/Delivery", statute="4759922b", level="Felony Class A", disposition=Dispositions.DISMISSED
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert type_eligibility.reason == "Dismissals are generally eligible under 137.225(1)(b)"


def test_manufacture_delivery_missing_disposition():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Manufacture/Delivery", statute="4759922b", level="Felony Class A", disposition=None
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Always eligible under 137.226 (for convictions) or 137.225(1)(b) (for dismissals) ⬥ Disposition not found. Needs further analysis"
    )


def test_manufacture_delivery_unrecognized_disposition():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Manufacture/Delivery",
        statute="4759922b",
        level="Felony Class B",
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Always eligible under 137.226 (for convictions) or 137.225(1)(b) (for dismissals) ⬥ Disposition not recognized. Needs further analysis"
    )


def test_manufacture_delivery_manudel():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Manu/Del Cntrld Sub-SC 1", statute="4759921B", level="Felony Class A", disposition=Dispositions.CONVICTED
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert type_eligibility.reason == "Eligible under 137.226 ⬥ Ineligible by omission from statute"


def test_manufacture_delivery_manudel_felony_unclassified():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Manu/Del Cntrld Sub-SC 1",
        statute="4759921B",
        level="Felony Unclassified",
        disposition=Dispositions.CONVICTED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Eligible under 137.226 ⬥ Ineligible by omission from statute ⬥ Convictions that fulfill the conditions of 137.225(5)(a) are eligible ⬥ Eligible under 137.225(5)(b)"
    )


def test_manufacture_delivery_manudel_felony_c():
    charges = ChargeFactory.create_ambiguous_charge(
        name="Manu/Del Cntrld Sub-SC 1", statute="4759921B", level="Felony Class C", disposition=Dispositions.CONVICTED
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert type_eligibility.reason == "Eligible under 137.225(5)(b)"


def test_manufacture_delivery_manufacturing_name():
    charges = ChargeFactory.create_ambiguous_charge(
        name="MANUFACTURING CONTROLLED SUB",
        statute="4759921A",
        level="Felony Unclassified",
        disposition=Dispositions.CONVICTED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Eligible under 137.226 ⬥ Ineligible by omission from statute ⬥ Convictions that fulfill the conditions of 137.225(5)(a) are eligible ⬥ Eligible under 137.225(5)(b)"
    )


def test_manufacture_delivery_1():
    charges = ChargeFactory.create_ambiguous_charge(
        name="MANUFACTURING CONTROLLED SUB 2",
        statute="4759921A",
        level="Felony Unclassified",
        disposition=Dispositions.CONVICTED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Ineligible by omission from statute ⬥ Convictions that fulfill the conditions of 137.225(5)(a) are eligible"
    )


def test_manufacture_delivery_heroin():
    charges = ChargeFactory.create_ambiguous_charge(
        name="MANUFACTURING CONTROLLED SUB HEROIN",
        statute="4759921A",
        level="Felony Unclassified",
        disposition=Dispositions.CONVICTED,
    )
    type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        type_eligibility.reason
        == "Ineligible by omission from statute ⬥ Convictions that fulfill the conditions of 137.225(5)(a) are eligible"
    )
