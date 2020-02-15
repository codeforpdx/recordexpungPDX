import unittest

from datetime import date

import pytest
from dateutil.relativedelta import relativedelta
from expungeservice.expunger import Expunger
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.factories.expunger_factory import ExpungerFactory
from tests.time import Time


class TestSingleChargeDismissals(unittest.TestCase):
    def setUp(self):
        self.expunger = ExpungerFactory.create()

    def test_eligible_arrests_eligibility_based_on_second_mrc(self):
        case = CaseFactory.create()

        three_yr_conviction = ChargeFactory.create(
            case=case, disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO)
        )

        arrest = ChargeFactory.create(case=case, disposition=Disposition(ruling="Dismissed", date=Time.THREE_YEARS_AGO))

        violation = ChargeFactory.create(
            level="Violation",
            case=case,
            disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
        )

        violation_2 = ChargeFactory.create(
            level="Violation",
            case=case,
            disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
        )

        case.charges = [three_yr_conviction, arrest, violation, violation_2]
        record = Record([case])
        expunger = Expunger(record)

        expunger.run()
        assert three_yr_conviction.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert three_yr_conviction.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(7)(b)"
        assert three_yr_conviction.expungement_result.time_eligibility.date_will_be_eligible == date.today() + relativedelta(
            years=7, days=1
        )

        assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert arrest.expungement_result.time_eligibility.date_will_be_eligible == date.today() + relativedelta(years=7)

    def test_ineligible_mrc_with_arrest_on_single_case(self):
        case = CaseFactory.create()

        mrc = ChargeFactory.create(
            case=case, disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO)
        )

        arrest = ChargeFactory.create(
            case=case, disposition=Disposition(ruling="Dismissed", date=Time.LESS_THAN_THREE_YEARS_AGO)
        )

        case.charges = [mrc, arrest]
        record = Record([case])
        expunger = Expunger(record)

        expunger.run()
        assert arrest.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert mrc.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert mrc.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(1)(a)"
        assert mrc.expungement_result.time_eligibility.date_will_be_eligible == date.today() + relativedelta(days=+1)

    def test_more_than_ten_year_old_conviction(self):
        case = CaseFactory.create()
        charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO))

        case.charges = [charge]
        record = Record([case])
        expunger = Expunger(record)
        expunger.run()

        assert charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.time_eligibility.reason == ""
        assert (
            charge.expungement_result.time_eligibility.date_will_be_eligible
            == charge.disposition.date + relativedelta(years=+3)
        )

    def test_10_yr_old_conviction_with_3_yr_old_mrc(self):
        case = CaseFactory.create()
        ten_yr_charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO))
        three_yr_mrc = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO))

        case.charges = [ten_yr_charge, three_yr_mrc]
        record = Record([case])
        expunger = Expunger(record)
        expunger.run()

        assert ten_yr_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert ten_yr_charge.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(7)(b)"
        assert (
            ten_yr_charge.expungement_result.time_eligibility.date_will_be_eligible
            == three_yr_mrc.disposition.date + Time.TEN_YEARS
        )

        assert three_yr_mrc.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert three_yr_mrc.expungement_result.time_eligibility.reason == ""
        assert (
            three_yr_mrc.expungement_result.time_eligibility.date_will_be_eligible
            == ten_yr_charge.disposition.date + Time.TEN_YEARS
        )

    def test_10_yr_old_conviction_with_less_than_3_yr_old_mrc(self):
        case = CaseFactory.create()
        ten_yr_charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO))
        less_than_three_yr_mrc = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO)
        )

        case.charges = [ten_yr_charge, less_than_three_yr_mrc]
        record = Record([case])
        expunger = Expunger(record)
        expunger.run()

        assert ten_yr_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert ten_yr_charge.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(7)(b)"
        assert (
            ten_yr_charge.expungement_result.time_eligibility.date_will_be_eligible
            == less_than_three_yr_mrc.disposition.date + Time.TEN_YEARS
        )

        assert less_than_three_yr_mrc.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert (
            less_than_three_yr_mrc.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(1)(a)"
        )
        assert less_than_three_yr_mrc.expungement_result.time_eligibility.date_will_be_eligible == date.today() + relativedelta(
            days=+1
        )

    def test_more_than_three_year_rule_conviction(self):
        case = CaseFactory.create()
        charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO))

        case.charges = [charge]
        record = Record([case])
        expunger = Expunger(record)
        expunger.run()

        assert charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.time_eligibility.reason == ""
        assert charge.expungement_result.time_eligibility.date_will_be_eligible == date.today()

    def test_less_than_three_year_rule_conviction(self):
        case = CaseFactory.create()
        charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO))

        case.charges = [charge]
        record = Record([case])
        expunger = Expunger(record)
        expunger.run()

        assert charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert charge.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(1)(a)"
        assert charge.expungement_result.time_eligibility.date_will_be_eligible == date.today() + relativedelta(days=+1)

    def test_time_eligibility_date_is_none_when_type_ineligible(self):
        case = CaseFactory.create()
        charge = ChargeFactory.create(
            name="Assault in the first degree",
            statute="163.185",
            level="Felony Class A",
            date=Time.ONE_YEAR_AGO,
            disposition=Disposition(ruling="Convicted", date=Time.ONE_YEAR_AGO),
        )

        case.charges = [charge]
        record = Record([case])
        expunger = Expunger(record)
        expunger.run()

        assert charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert (
            charge.expungement_result.time_eligibility.reason
            == "Never. Type ineligible charges are always time ineligible."
        )
        assert charge.expungement_result.time_eligibility.date_will_be_eligible is date.max


class TestDismissalBlock(unittest.TestCase):
    def setUp(self):
        self.case_1 = CaseFactory.create()
        self.case_2 = CaseFactory.create()

        self.recent_dismissal = ChargeFactory.create_dismissed_charge(case=self.case_1, date=Time.TWO_YEARS_AGO)
        self.case_1.charges = [self.recent_dismissal]

    def test_record_with_only_an_mrd_is_time_eligible(self):
        record = Record([self.case_1])
        expunger = Expunger(record)
        expunger.run()

        assert self.recent_dismissal.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert self.recent_dismissal.expungement_result.time_eligibility.reason == ""
        assert self.recent_dismissal.expungement_result.time_eligibility.date_will_be_eligible == Time.TWO_YEARS_AGO

    def test_all_mrd_case_related_dismissals_are_expungeable(self):
        case_related_dismissal = ChargeFactory.create_dismissed_charge(case=self.case_1, date=Time.TWO_YEARS_AGO)
        self.case_1.charges.append(case_related_dismissal)

        record = Record([self.case_1])
        expunger = Expunger(record)
        expunger.run()

        assert self.recent_dismissal.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert self.recent_dismissal.expungement_result.time_eligibility.reason == ""
        assert self.recent_dismissal.expungement_result.time_eligibility.date_will_be_eligible == Time.TWO_YEARS_AGO

        assert case_related_dismissal.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert case_related_dismissal.expungement_result.time_eligibility.reason == ""
        assert case_related_dismissal.expungement_result.time_eligibility.date_will_be_eligible == Time.TWO_YEARS_AGO

    def test_mrd_blocks_dismissals_in_unrelated_cases(self):
        unrelated_dismissal = ChargeFactory.create_dismissed_charge(case=self.case_2, date=Time.TEN_YEARS_AGO)
        self.case_2.charges = [unrelated_dismissal]

        record = Record([self.case_1, self.case_2])
        expunger = Expunger(record)
        expunger.run()

        assert unrelated_dismissal.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert unrelated_dismissal.expungement_result.time_eligibility.reason == "Recommend sequential expungement"
        assert unrelated_dismissal.expungement_result.time_eligibility.date_will_be_eligible == Time.ONE_YEARS_FROM_NOW

    def test_mrd_does_not_block_convictions(self):
        case = CaseFactory.create()
        convicted_charge = ChargeFactory.create(
            case=case,
            date=Time.TWENTY_YEARS_AGO,
            disposition=Disposition(ruling="Convicted", date=Time.TWENTY_YEARS_AGO),
        )
        case.charges = [convicted_charge]

        record = Record([self.case_1, case])
        expunger = Expunger(record)
        expunger.run()

        assert convicted_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
        assert convicted_charge.expungement_result.time_eligibility.reason == ""
        assert (
            convicted_charge.expungement_result.time_eligibility.date_will_be_eligible
            == convicted_charge.disposition.date + relativedelta(years=+3)
        )


class TestSecondMRCLogic(unittest.TestCase):
    def setUp(self):
        self.expunger = ExpungerFactory.create()

    def run_expunger(self, mrc, second_mrc):
        case = CaseFactory.create()
        case.charges = [mrc, second_mrc]
        record = Record([case])
        expunger = Expunger(record)
        expunger.run()

    def test_3_yr_old_conviction_2_yr_old_mrc(self):
        three_years_ago_charge = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO)
        )
        two_years_ago_charge = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.TWO_YEARS_AGO)
        )

        self.run_expunger(two_years_ago_charge, three_years_ago_charge)

        assert three_years_ago_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert (
            three_years_ago_charge.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(7)(b)"
        )
        assert (
            three_years_ago_charge.expungement_result.time_eligibility.date_will_be_eligible
            == two_years_ago_charge.disposition.date + Time.TEN_YEARS
        )

        assert two_years_ago_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert two_years_ago_charge.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(7)(b)"
        assert (
            two_years_ago_charge.expungement_result.time_eligibility.date_will_be_eligible
            == three_years_ago_charge.disposition.date + Time.TEN_YEARS
        )

    def test_7_yr_old_conviction_5_yr_old_mrc(self):
        seven_year_ago_charge = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.SEVEN_YEARS_AGO)
        )
        five_year_ago_charge = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.FIVE_YEARS_AGO)
        )

        self.run_expunger(five_year_ago_charge, seven_year_ago_charge)

        assert seven_year_ago_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert seven_year_ago_charge.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(7)(b)"
        assert (
            seven_year_ago_charge.expungement_result.time_eligibility.date_will_be_eligible
            == five_year_ago_charge.disposition.date + Time.TEN_YEARS
        )

        assert five_year_ago_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
        assert five_year_ago_charge.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(7)(b)"
        assert (
            five_year_ago_charge.expungement_result.time_eligibility.date_will_be_eligible
            == seven_year_ago_charge.disposition.date + Time.TEN_YEARS
        )

    def test_mrc_is_eligible_in_two_years(self):
        nine_year_old_conviction = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.NINE_YEARS_AGO)
        )
        one_year_old_conviction = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.ONE_YEAR_AGO)
        )
        eligibility_date = one_year_old_conviction.disposition.date + Time.THREE_YEARS

        self.run_expunger(one_year_old_conviction, nine_year_old_conviction)

        assert one_year_old_conviction.expungement_result.time_eligibility.date_will_be_eligible == eligibility_date


def create_class_b_felony_charge(date, ruling="Convicted"):
    return ChargeFactory.create(
        name="Aggravated theft in the first degree",
        statute="164.057",
        level="Felony Class B",
        date=date,
        disposition=Disposition(ruling=ruling, date=date),
    )


def test_felony_class_b_greater_than_20yrs():
    case = CaseFactory.create()
    charge = create_class_b_felony_charge(Time.TWENTY_YEARS_AGO)
    case.charges = [charge]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert charge.expungement_result.time_eligibility.reason == ""
    assert charge.expungement_result.time_eligibility.date_will_be_eligible == date.today()


def test_felony_class_b_less_than_20yrs():
    case = CaseFactory.create()
    charge = create_class_b_felony_charge(Time.LESS_THAN_TWENTY_YEARS_AGO)
    case.charges = [charge]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        charge.expungement_result.time_eligibility.reason
        == "137.225(5)(a)(A)(i) - Twenty years from class B felony conviction"
    )
    assert charge.expungement_result.time_eligibility.date_will_be_eligible == Time.TOMORROW


def test_felony_class_b_with_subsequent_conviction():
    b_felony_charge = create_class_b_felony_charge(Time.TWENTY_YEARS_AGO)
    case_1 = CaseFactory.create()
    case_1.charges = [b_felony_charge]
    subsequent_charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO))
    case_2 = CaseFactory.create()
    case_2.charges = [subsequent_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger.run()

    assert b_felony_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        b_felony_charge.expungement_result.time_eligibility.reason
        == "Never. Class B felony can have no subsequent arrests or convictions (137.225(5)(a)(A)(ii))"
    )
    assert b_felony_charge.expungement_result.time_eligibility.date_will_be_eligible == date.max

    # The Class B felony does not affect eligibility of another charge that is otherwise eligible
    assert subsequent_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert subsequent_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE


def test_felony_class_b_with_prior_conviction():
    b_felony_charge = create_class_b_felony_charge(Time.TWENTY_YEARS_AGO)
    case_1 = CaseFactory.create()
    case_1.charges = [b_felony_charge]
    prior_charge = ChargeFactory.create(
        disposition=Disposition(ruling="Convicted", date=Time.MORE_THAN_TWENTY_YEARS_AGO)
    )
    case_2 = CaseFactory.create()
    case_2.charges = [prior_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger.run()

    assert b_felony_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
    assert b_felony_charge.expungement_result.type_eligibility.reason == "Further Analysis Needed"
    assert b_felony_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert b_felony_charge.expungement_result.time_eligibility.reason == ""


def test_dismissed_felony_class_b_with_subsequent_conviction():
    b_felony_charge = create_class_b_felony_charge(Time.LESS_THAN_TWENTY_YEARS_AGO, "Dismissed")
    case_1 = CaseFactory.create()
    case_1.charges = [b_felony_charge]
    subsequent_charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO))
    case_2 = CaseFactory.create()
    case_2.charges = [subsequent_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger.run()

    assert b_felony_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert b_felony_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE


def test_doubly_eligible_b_felony_gets_normal_eligibility_rule():
    # This charge is both Subsection 12 and also a class B felony. List B classification takes precedence.
    subsection_12_charge = ChargeFactory.create(
        name="Assault in the second degree",
        statute="163.175",
        level="Felony Class B",
        date=Time.LESS_THAN_TWENTY_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_TWENTY_YEARS_AGO),
    )

    case_1 = CaseFactory.create()
    case_1.charges = [subsection_12_charge]
    subsequent_charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO))
    case_2 = CaseFactory.create()
    case_2.charges = [subsequent_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger.run()

    assert subsection_12_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
    assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE


def test_single_violation_is_time_restricted():
    # A single violation doesn't block other records, but it is still subject to the 3 year rule.
    violation_charge = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TEN_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
    )

    case = CaseFactory.create()
    case.charges = [violation_charge]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert violation_charge.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert violation_charge.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(1)(a)"
    assert violation_charge.expungement_result.time_eligibility.date_will_be_eligible == date.today() + relativedelta(
        days=+1
    )


def test_2_violations_are_time_restricted():
    violation_charge_1 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.LESS_THAN_THREE_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
    )
    violation_charge_2 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TWO_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.TWO_YEARS_AGO),
    )

    case = CaseFactory.create()
    case.charges = [violation_charge_1, violation_charge_2]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert violation_charge_1.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert violation_charge_1.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(1)(a)"
    assert (
        violation_charge_1.expungement_result.time_eligibility.date_will_be_eligible
        == violation_charge_1.disposition.date + Time.THREE_YEARS
    )

    assert violation_charge_2.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert violation_charge_2.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(1)(a)"
    assert (
        violation_charge_2.expungement_result.time_eligibility.date_will_be_eligible
        == violation_charge_2.disposition.date + Time.THREE_YEARS
    )


def test_3_violations_are_time_restricted():
    violation_charge_1 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.LESS_THAN_THREE_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
    )
    violation_charge_2 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TWO_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.TWO_YEARS_AGO),
    )
    violation_charge_3 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.ONE_YEAR_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.ONE_YEAR_AGO),
    )

    case = CaseFactory.create()
    case.charges = [violation_charge_3, violation_charge_2, violation_charge_1]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert violation_charge_1.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert violation_charge_1.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(7)(b)"
    assert (
        violation_charge_1.expungement_result.time_eligibility.date_will_be_eligible
        == violation_charge_2.disposition.date + Time.TEN_YEARS
    )

    assert violation_charge_2.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert violation_charge_2.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(7)(b)"
    assert (
        violation_charge_2.expungement_result.time_eligibility.date_will_be_eligible
        == violation_charge_1.disposition.date + Time.TEN_YEARS
    )

    assert violation_charge_3.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert violation_charge_3.expungement_result.time_eligibility.reason == "Time-ineligible under 137.225(7)(b)"
    assert (
        violation_charge_3.expungement_result.time_eligibility.date_will_be_eligible
        == violation_charge_1.disposition.date + Time.TEN_YEARS
    )


def test_nonblocking_charge_is_not_skipped_and_does_not_block():
    civil_offense = ChargeFactory.create(
        level="N/A", statute="1.000", disposition=Disposition(ruling="Convicted", date=Time.ONE_YEAR_AGO)
    )

    violation_charge = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TEN_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO),
    )

    case = CaseFactory.create()
    case.charges = [civil_offense, violation_charge]
    expunger = Expunger(Record([case]))
    expunger.run()

    assert civil_offense.expungement_result.time_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        civil_offense.expungement_result.time_eligibility.reason
        == "Never. Type ineligible charges are always time ineligible."
    )
    assert civil_offense.expungement_result.time_eligibility.date_will_be_eligible == date.max

    assert violation_charge.expungement_result.time_eligibility.status is EligibilityStatus.ELIGIBLE
