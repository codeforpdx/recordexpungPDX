
from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


def build_charge(statute, disposition_ruling):
    last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
    charge = ChargeFactory.build()
    charge['statute'] = statute
    charge['disposition'] = Disposition(ruling=disposition_ruling, date=last_week)
    return ChargeFactory.save(charge)


def test_duii_acquitted():

    duii_acquitted = build_charge(statute = "813.010", disposition_ruling = "Acquitted")

    assert duii_acquitted.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert duii_acquitted.expungement_result.type_eligibility.reason == 'Further Analysis Needed'


def test_duii_diverted():

    duii_diverted = build_charge(statute = "813.011", disposition_ruling = "Diverted")

    assert duii_diverted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert duii_diverted.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(8)(b)'


def test_duii_convicted():

    duii_convicted = build_charge(statute = "813.123", disposition_ruling = "Convicted")

    assert duii_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert duii_convicted.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(7)(a)'
