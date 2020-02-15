from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


def build_charge(statute, disposition_ruling):
    last_week = datetime.today() - timedelta(days=7)
    charge = ChargeFactory.build()
    charge["statute"] = statute
    charge["disposition"] = Disposition(ruling=disposition_ruling, date=last_week)
    return ChargeFactory.save(charge)


def test_duii_dismissed():
    duii_dismissed = build_charge(statute="813.010", disposition_ruling="Acquitted")

    assert duii_dismissed.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert (
        duii_dismissed.expungement_result.type_eligibility.reason
        == "Further Analysis Needed - Dismissed charge may have been Diverted"
    )


def test_duii_diverted():
    duii_diverted = build_charge(statute="813.011", disposition_ruling="Diverted")

    assert duii_diverted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        duii_diverted.expungement_result.type_eligibility.reason
        == "137.225(8)(b) - Diverted DUII charges are ineligible"
    )


def test_duii_convicted():
    duii_convicted = build_charge(statute="813.123", disposition_ruling="Convicted")

    assert duii_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        duii_convicted.expungement_result.type_eligibility.reason == "137.225(7)(a) - Traffic offenses are ineligible"
    )
