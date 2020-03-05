from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge
from expungeservice.models.expungement_result import EligibilityStatus
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions


def test_unclassified_charge():
    unclassified_dismissed = ChargeFactory.create(
        name="Assault in the ninth degree",
        statute="333.333",
        level="Felony Class F",
        disposition=Dispositions.DISMISSED,
    )

    assert isinstance(unclassified_dismissed, UnclassifiedCharge)
    assert unclassified_dismissed.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        unclassified_dismissed.expungement_result.type_eligibility.reason
        == "Unrecognized Charge : Further Analysis Needed"
    )


def test_charge_that_falls_through():
    charge = ChargeFactory.create(
        name="Aggravated theft in the first degree",
        statute="164.057",
        level="Felony Class F",
        disposition=Dispositions.DISMISSED,
    )

    assert isinstance(charge, UnclassifiedCharge)
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert charge.expungement_result.type_eligibility.reason == "Unrecognized Charge : Further Analysis Needed"
