from expungeservice.util import DateWithFuture as date
from dateutil.relativedelta import relativedelta

from expungeservice.models.disposition import DispositionCreator
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.record_merger import RecordMerger

from tests.factories.charge_factory import ChargeFactory


def build_charges(statute, disposition_ruling):
    last_week = date.today() - relativedelta(days=7)
    return ChargeFactory.create_ambiguous_charge(
        statute=statute, disposition=DispositionCreator.create(ruling=disposition_ruling, date=last_week)
    )


def test_duii_dismissed():
    charges = build_charges(statute="813.010", disposition_ruling="Acquitted")
    duii_type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert duii_type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        duii_type_eligibility.reason
        == "Diverted DUII – Ineligible under 137.225(8) OR Dismissed Criminal Charge – Dismissals are generally eligible under 137.225(1)(d)"
    )


def test_duii_diverted():
    charges = build_charges(statute="813.011", disposition_ruling="Diverted")
    duii_type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert duii_type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        duii_type_eligibility.reason
        == "Diverted DUII – Ineligible under 137.225(8) OR Dismissed Criminal Charge – Dismissals are generally eligible under 137.225(1)(d)"
    )


def test_duii_convicted():
    charges = build_charges(statute="813.123", disposition_ruling="Convicted")
    duii_type_eligibility = RecordMerger.merge_type_eligibilities(charges)

    assert duii_type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert duii_type_eligibility.reason == "DUII – Traffic offenses are ineligible under 137.225(7)(a)"
