
from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


def test_duii_acquitted():

    last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
    single_charge = ChargeFactory.build()

    single_charge['statute'] = '813.010'
    single_charge['disposition'] = Disposition(ruling='Acquitted', date=last_week)

    duii_acquitted = ChargeFactory.save(single_charge)

    assert duii_acquitted.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert duii_acquitted.expungement_result.type_eligibility.reason == 'Further Analysis Needed'

def test_duii_diverted():

    last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
    single_charge = ChargeFactory.build()

    single_charge['statute'] = '813.011'
    single_charge['disposition'] = Disposition(ruling='Diverted', date=last_week)

    duii_diverted = ChargeFactory.save(single_charge)

    assert duii_diverted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert duii_diverted.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(8)(b)'


def test_duii_convicted():

    last_week = (datetime.today() - timedelta(days=7)).strftime('%m/%d/%Y')
    single_charge = ChargeFactory.build()

    single_charge['statute'] = '813.123'
    single_charge['disposition'] = Disposition(ruling='Convicted', date=last_week)

    duii_convicted = ChargeFactory.save(single_charge)

    assert duii_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert duii_convicted.expungement_result.type_eligibility.reason == 'Ineligible under 137.225(7)(a)'

