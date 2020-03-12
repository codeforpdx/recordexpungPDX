from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaEligible
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
import pytest


def test_delivery_to_minor_4758604A():
    marijuana_eligible_charge = ChargeFactory.create(
        name="Delivery of Marijuana to Minor",
        statute="4758604A",
        level="Felony Class A",
        disposition=Dispositions.DISMISSED,
    )
    assert isinstance(marijuana_eligible_charge, MarijuanaEligible)
    assert marijuana_eligible_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert marijuana_eligible_charge.type_eligibility.reason == "Dismissals are eligible under 137.225(1)(b)"


def test_marijuana_eligible_convicted():
    marijuana_eligible_charge = ChargeFactory.create(
        name="Delivery of Marijuana to Minor",
        statute="4758604A",
        level="Felony Class A",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(marijuana_eligible_charge, MarijuanaEligible)
    assert marijuana_eligible_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert marijuana_eligible_charge.type_eligibility.reason == "Eligible under 137.226"


def test_marijuana_eligible_missing_dispo():
    marijuana_eligible_charge = ChargeFactory.create(
        name="Delivery of Marijuana to Minor", statute="4758604A", level="Felony Class A", disposition=None
    )

    assert isinstance(marijuana_eligible_charge, MarijuanaEligible)
    assert marijuana_eligible_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        marijuana_eligible_charge.type_eligibility.reason
        == "Always eligible under 137.226 (for convictions) or 137.225(1)(b) (for dismissals)"
    )


def test_marijuana_eligible_unrecognized_dispo():
    marijuana_eligible_charge = ChargeFactory.create(
        name="Delivery of Marijuana to Minor",
        statute="4758604A",
        level="Felony Class A",
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
    )

    assert isinstance(marijuana_eligible_charge, MarijuanaEligible)
    assert marijuana_eligible_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        marijuana_eligible_charge.type_eligibility.reason
        == "Always eligible under 137.226 (for convictions) or 137.225(1)(b) (for dismissals)"
    )


def test_delivery_4758602():
    marijuana_eligible_charge = ChargeFactory.create(
        name="Delivery of Marijuana for Consideration",
        statute="4758602",
        level="Felony Class B",
        disposition=Dispositions.CONVICTED,
    )

    assert isinstance(marijuana_eligible_charge, MarijuanaEligible)
