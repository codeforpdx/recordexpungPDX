from datetime import date
from dateutil.relativedelta import relativedelta
from expungeservice.expunger.expunger import Expunger
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.expunger_factory import ExpungerFactory
from tests.utilities.time import Time

def create_class_b_felony_charge(date, ruling='Convicted'):
    return ChargeFactory.create(name='Aggravated theft in the first degree',
                                  statute='164.057',
                                  level='Felony Class B',
                                  date=date,
                                  disposition=[ruling, date])

def test_felony_class_b_greater_than_20yrs():
    case = CaseFactory.create()
    charge = create_class_b_felony_charge(Time.TWENTY_YEARS_AGO)
    case.charges = [charge]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.expungement_result.time_eligibility.reason == ''
    assert charge.expungement_result.time_eligibility.date_will_be_eligible is None

def test_felony_class_b_less_than_20yrs():
    case = CaseFactory.create()
    charge = create_class_b_felony_charge(Time.LESS_THAN_TWENTY_YEARS_AGO)
    case.charges = [charge]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.expungement_result.time_eligibility.reason == '137.225(5)(a)(A)(i) - Twenty years from class B felony conviction'
    assert charge.expungement_result.time_eligibility.date_will_be_eligible == Time.TOMORROW

def test_felony_class_b_with_subsequent_conviction():
    b_felony_charge = create_class_b_felony_charge(Time.TWENTY_YEARS_AGO)
    case_1 = CaseFactory.create()
    case_1.charges=[b_felony_charge]
    subsequent_charge = ChargeFactory.create(disposition=['Convicted', Time.TEN_YEARS_AGO])
    case_2 = CaseFactory.create()
    case_2.charges=[subsequent_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger.run()

    assert b_felony_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert b_felony_charge.expungement_result.time_eligibility == None
    assert b_felony_charge.expungement_result.type_eligibility.reason == (
        "137.225(5)(a)(A)(ii) - Class B felony can have no subsequent arrests or convictions")

    # The Class B felony does not affect eligibility of another charge that is otherwise eligible
    assert subsequent_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert subsequent_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE

def test_felony_class_b_with_prior_conviction():
    b_felony_charge = create_class_b_felony_charge(Time.TWENTY_YEARS_AGO)
    case_1 = CaseFactory.create()
    case_1.charges=[b_felony_charge]
    prior_charge = ChargeFactory.create(disposition=['Convicted', Time.OVER_TWENTY_YEARS_AGO])
    case_2 = CaseFactory.create()
    case_2.charges=[prior_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger.run()

    assert b_felony_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert b_felony_charge.expungement_result.type_eligibility.reason == 'Further Analysis Needed'
    assert b_felony_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert b_felony_charge.expungement_result.time_eligibility.reason == ''

def test_acquitted_felony_class_b_with_subsequent_conviction():
    b_felony_charge = create_class_b_felony_charge(Time.TWENTY_YEARS_AGO, 'Dismissed')
    case_1 = CaseFactory.create()
    case_1.charges=[b_felony_charge]
    subsequent_charge = ChargeFactory.create(disposition=['Convicted', Time.TEN_YEARS_AGO])
    case_2 = CaseFactory.create()
    case_2.charges=[subsequent_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger.run()

    assert b_felony_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert b_felony_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE

def test_doubly_eligible_b_felony_gets_normal_eligibility_rule():
    # This charge is both List B and also a class B felony. List B classification takes precedence.
    list_b_charge = ChargeFactory.create(name='Assault in the second degree',
                                  statute='163.175',
                                  level='Felony Class B',
                                  date=Time.LESS_THAN_TWENTY_YEARS_AGO,
                                  disposition=['Convicted', Time.LESS_THAN_TWENTY_YEARS_AGO])

    case_1 = CaseFactory.create()
    case_1.charges=[list_b_charge]
    subsequent_charge = ChargeFactory.create(disposition=['Convicted', Time.TEN_YEARS_AGO])
    case_2 = CaseFactory.create()
    case_2.charges=[subsequent_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger.run()

    assert list_b_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert list_b_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
