from expungeservice.models.charge_types.dismissed_charge import DismissedCharge
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
    assert unclassified_dismissed.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert unclassified_dismissed.type_eligibility.reason == "Unrecognized Charge : Further Analysis Needed"


def test_charge_that_falls_through():
    charge = ChargeFactory.create(
        name="Aggravated theft in the first degree",
        statute="164.057",
        level="Felony Class F",
        disposition=Dispositions.DISMISSED,
    )

    assert isinstance(charge, UnclassifiedCharge)
    assert charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert charge.type_eligibility.reason == "Unrecognized Charge : Further Analysis Needed"


def test_unrecognized_disposition():
    unclassified_dismissed = ChargeFactory.create(
        name="Unknown", statute="333.333", level="Felony Class F", disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
    )
    assert isinstance(unclassified_dismissed, UnclassifiedCharge)
    assert unclassified_dismissed.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert unclassified_dismissed.type_eligibility.reason == "Unrecognized Charge : Further Analysis Needed"


def test_convicted_disposition():
    unclassified_convicted = ChargeFactory.create(
        name="Unknown", statute="333.333", level="Felony Class F", disposition=Dispositions.CONVICTED,
    )

    assert isinstance(unclassified_convicted, UnclassifiedCharge)
    assert unclassified_convicted.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert unclassified_convicted.type_eligibility.reason == "Unrecognized Charge : Further Analysis Needed"


def test_no_disposition():
    unclassified_dispo_none = ChargeFactory.create(
        name="Unknown", statute="333.333", level="Felony Class F", disposition=None,
    )

    assert isinstance(unclassified_dispo_none, UnclassifiedCharge)
    assert unclassified_dispo_none.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert unclassified_dispo_none.type_eligibility.reason == "Unrecognized Charge : Further Analysis Needed"
