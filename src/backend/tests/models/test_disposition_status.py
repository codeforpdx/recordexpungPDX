from datetime import date

from expungeservice.models.disposition import Disposition, DispositionStatus
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory


def test_disposition_status_values():
    today = date.today().strftime('%m/%d/%Y')

    assert Disposition(today, 'Dismissed').status == DispositionStatus.DISMISSED
    assert Disposition(today, 'Dismissal').status == DispositionStatus.DISMISSED
    assert Disposition(today, 'Acquitted').status == DispositionStatus.DISMISSED
    assert Disposition(today, 'Acquittal').status == DispositionStatus.DISMISSED

    assert Disposition(today, 'Convicted').status == DispositionStatus.CONVICTED
    assert Disposition(today, 'Reduced to a lesser charge').status == DispositionStatus.CONVICTED
    assert Disposition(today, 'Conversion - Disposition Types').status == DispositionStatus.CONVICTED

    assert Disposition(today, 'Diverted').status == DispositionStatus.DIVERTED

    assert Disposition(today, 'No complaint').status == DispositionStatus.NO_COMPLAINT

    assert Disposition(today, 'What is this?').status == DispositionStatus.UNKNOWN


def test_all_disposition_statuses_are_either_convicted_or_acquitted():

    charge = ChargeFactory.create()
    today = date.today().strftime('%m/%d/%Y')

    for status in DispositionStatus:
        # Use the status.value to create the disposition,
        # which happens to always be a valid string for that dispo status.
        charge.disposition = Disposition(today, status.value)

        if status == DispositionStatus.UNKNOWN:
            assert not charge.convicted()
            assert not charge.acquitted()

        else:
            # Make sure that every DispositionStatus value is covered by this approach.
            assert charge.disposition.status == status
            assert charge.convicted() or charge.acquitted()

def test_dispositionless_charge_is_not_convicted_nor_acquitted():
    charge = ChargeFactory.create()
    assert not charge.convicted()
    assert not charge.acquitted()
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert charge.expungement_result.type_eligibility.reason == "Disposition not found. Needs further analysis"

def test_charge_with_unknown_disposition_eligibility():
    charge = ChargeFactory.create(disposition=["What am I", "1/1/0001"])
    assert not charge.convicted()
    assert not charge.acquitted()
    assert charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert charge.expungement_result.type_eligibility.reason == "Disposition not recognized. Needs further analysis"