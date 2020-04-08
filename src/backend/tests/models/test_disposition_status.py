from dataclasses import replace
from datetime import date

from expungeservice.models.disposition import DispositionStatus, DispositionCreator
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory


def test_disposition_status_values():
    today = date.today()
    assert DispositionCreator.create(today, "Dismissed").status == DispositionStatus.DISMISSED
    assert DispositionCreator.create(today, "Dismissal").status == DispositionStatus.DISMISSED
    assert DispositionCreator.create(today, "Acquitted").status == DispositionStatus.DISMISSED
    assert DispositionCreator.create(today, "Acquittal").status == DispositionStatus.DISMISSED
    assert DispositionCreator.create(today, "Convicted").status == DispositionStatus.CONVICTED
    assert DispositionCreator.create(today, "Reduced to a lesser charge").status == DispositionStatus.CONVICTED
    assert DispositionCreator.create(today, "Conversion - Disposition Types").status == DispositionStatus.CONVICTED
    assert DispositionCreator.create(today, "Diverted").status == DispositionStatus.DIVERTED
    assert DispositionCreator.create(today, "No complaint").status == DispositionStatus.NO_COMPLAINT
    assert DispositionCreator.create(today, "What is this?").status == DispositionStatus.UNRECOGNIZED


def test_all_disposition_statuses_are_either_convicted_or_dismissed():
    pre_charge = ChargeFactory.create()
    today = date.today()
    for status in DispositionStatus:
        # Use the status.value to create the disposition,
        # which happens to always be a valid string for that dispo status.
        charge = replace(pre_charge, disposition=DispositionCreator.create(today, status.value))

        if status == DispositionStatus.UNRECOGNIZED:
            assert not charge.convicted()
            assert not charge.dismissed()
        else:
            # Make sure that every DispositionStatus value is covered by this approach.
            assert charge.disposition.status == status
            assert charge.convicted() or charge.dismissed()


def test_dispositionless_charge_is_not_convicted_nor_dismissed():
    charge = ChargeFactory.create(level="Felony Class B")

    assert not charge.convicted()
    assert not charge.dismissed()
    assert charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert charge.type_eligibility.reason == "Disposition not found. Needs further analysis"


def test_charge_with_unrecognized_disposition_eligibility():
    charge = ChargeFactory.create(
        level="Felony Class B", disposition=DispositionCreator.create(ruling="What am I", date=date(2001, 1, 1))
    )
    assert not charge.convicted()
    assert not charge.dismissed()
    assert charge.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert charge.type_eligibility.reason == "Disposition not recognized. Needs further analysis"
