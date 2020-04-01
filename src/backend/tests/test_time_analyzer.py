import unittest

from datetime import date

from dateutil.relativedelta import relativedelta
from expungeservice.expunger import Expunger
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Record
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.time import Time


class TestSingleChargeDismissals(unittest.TestCase):
    def test_eligible_arrests_eligibility_based_on_second_mrc(self):
        case = CaseFactory.create()

        three_yr_conviction = ChargeFactory.create(
            case_number=case.case_number, disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO)
        )

        arrest = ChargeFactory.create(
            case_number=case.case_number, disposition=Disposition(ruling="Dismissed", date=Time.THREE_YEARS_AGO)
        )

        violation = ChargeFactory.create(
            level="Violation",
            case_number=case.case_number,
            disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
        )

        violation_2 = ChargeFactory.create(
            level="Violation",
            case_number=case.case_number,
            disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
        )

        case.charges = [three_yr_conviction, arrest, violation, violation_2]
        record = Record([case])
        expunger = Expunger(record)

        expunger_result = expunger.run()
        assert expunger_result[three_yr_conviction.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[three_yr_conviction.ambiguous_charge_id].reason
            == "Ten years from most recent other conviction (137.225(7)(b))"
        )
        assert expunger_result[
            three_yr_conviction.ambiguous_charge_id
        ].date_will_be_eligible == date.today() + relativedelta(years=7, days=1)

        assert expunger_result[arrest.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert expunger_result[arrest.ambiguous_charge_id].date_will_be_eligible == date.today() + relativedelta(
            years=7
        )

    def test_ineligible_mrc_with_arrest_on_single_case(self):
        # In this case, the friendly rule doesn't apply because the conviction doesn't become eligible
        case = CaseFactory.create()

        mrc = ChargeFactory.create(
            case_number=case.case_number,
            disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
            statute="666.666",
            level="Felony Class A",
        )

        arrest = ChargeFactory.create(
            case_number=case.case_number,
            disposition=Disposition(ruling="Dismissed", date=Time.LESS_THAN_THREE_YEARS_AGO),
        )

        case.charges = [mrc, arrest]
        record = Record([case])
        expunger = Expunger(record)

        expunger_result = expunger.run()
        assert expunger_result[arrest.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[arrest.ambiguous_charge_id].reason
            == "Ten years from most recent conviction (137.225(7)(b))"
        )
        assert expunger_result[mrc.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[mrc.ambiguous_charge_id].reason
            == "Never. Type ineligible charges are always time ineligible."
        )
        assert expunger_result[mrc.ambiguous_charge_id].date_will_be_eligible == date.max

    def test_more_than_ten_year_old_conviction(self):
        case = CaseFactory.create()
        charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO))

        case.charges = [charge]
        record = Record([case])
        expunger = Expunger(record)
        expunger_result = expunger.run()

        assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[charge.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[
            charge.ambiguous_charge_id
        ].date_will_be_eligible == charge.disposition.date + relativedelta(years=+3)

    def test_10_yr_old_conviction_with_3_yr_old_mrc(self):
        case = CaseFactory.create()
        ten_yr_charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO))
        three_yr_mrc = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO))

        case.charges = [ten_yr_charge, three_yr_mrc]
        record = Record([case])
        expunger = Expunger(record)
        expunger_result = expunger.run()

        assert expunger_result[ten_yr_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[ten_yr_charge.ambiguous_charge_id].reason
            == "Ten years from most recent other conviction (137.225(7)(b))"
        )
        assert (
            expunger_result[ten_yr_charge.ambiguous_charge_id].date_will_be_eligible
            == three_yr_mrc.disposition.date + Time.TEN_YEARS
        )

        assert expunger_result[three_yr_mrc.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[three_yr_mrc.ambiguous_charge_id].reason == "Eligible now"
        assert (
            expunger_result[three_yr_mrc.ambiguous_charge_id].date_will_be_eligible
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
        expunger_result = expunger.run()

        assert expunger_result[ten_yr_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[ten_yr_charge.ambiguous_charge_id].reason
            == "Ten years from most recent other conviction (137.225(7)(b))"
        )
        assert (
            expunger_result[ten_yr_charge.ambiguous_charge_id].date_will_be_eligible
            == less_than_three_yr_mrc.disposition.date + Time.TEN_YEARS
        )

        assert expunger_result[less_than_three_yr_mrc.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[less_than_three_yr_mrc.ambiguous_charge_id].reason
            == "Three years from date of conviction (137.225(1)(a))"
        )
        assert expunger_result[
            less_than_three_yr_mrc.ambiguous_charge_id
        ].date_will_be_eligible == date.today() + relativedelta(days=+1)

    def test_more_than_three_year_rule_conviction(self):
        case = CaseFactory.create()
        charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO))

        case.charges = [charge]
        record = Record([case])
        expunger = Expunger(record)
        expunger_result = expunger.run()

        assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[charge.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible == date.today()

    def test_less_than_three_year_rule_conviction(self):
        case = CaseFactory.create()
        charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO))

        case.charges = [charge]
        record = Record([case])
        expunger = Expunger(record)
        expunger_result = expunger.run()

        assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[charge.ambiguous_charge_id].reason == "Three years from date of conviction (137.225(1)(a))"
        )
        assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible == date.today() + relativedelta(
            days=+1
        )

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
        expunger_result = expunger.run()

        assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[charge.ambiguous_charge_id].reason
            == "Never. Type ineligible charges are always time ineligible."
        )
        assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible is date.max


class TestDismissalBlock(unittest.TestCase):
    def setUp(self):
        self.case_1 = CaseFactory.create(case_number="1")
        self.case_2 = CaseFactory.create(case_number="2")

        self.recent_dismissal = ChargeFactory.create_dismissed_charge(
            case_number=self.case_1.case_number, date=Time.TWO_YEARS_AGO, violation_type=self.case_1.violation_type
        )
        self.case_1.charges = [self.recent_dismissal]

    def test_record_with_only_an_mrd_is_time_eligible(self):
        record = Record([self.case_1])
        expunger = Expunger(record)
        expunger_result = expunger.run()

        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].date_will_be_eligible == Time.TWO_YEARS_AGO

    def test_all_mrd_case_related_dismissals_are_expungeable(self):
        case_related_dismissal = ChargeFactory.create_dismissed_charge(
            case_number=self.case_1.case_number, date=Time.TWO_YEARS_AGO, violation_type=self.case_1.violation_type
        )
        self.case_1.charges.append(case_related_dismissal)

        record = Record([self.case_1])
        expunger = Expunger(record)
        expunger_result = expunger.run()

        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].date_will_be_eligible == Time.TWO_YEARS_AGO

        assert expunger_result[case_related_dismissal.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[case_related_dismissal.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[case_related_dismissal.ambiguous_charge_id].date_will_be_eligible == Time.TWO_YEARS_AGO

    def test_mrd_blocks_dismissals_in_unrelated_cases(self):
        unrelated_dismissal = ChargeFactory.create_dismissed_charge(
            case_number=self.case_2.case_number, date=Time.TEN_YEARS_AGO, violation_type=self.case_2.violation_type
        )
        self.case_2.charges = [unrelated_dismissal]

        record = Record([self.case_1, self.case_2])
        expunger = Expunger(record)
        expunger_result = expunger.run()

        assert expunger_result[unrelated_dismissal.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[unrelated_dismissal.ambiguous_charge_id].reason
            == "Three years from most recent other arrest (137.225(8)(a))"
        )
        assert expunger_result[unrelated_dismissal.ambiguous_charge_id].date_will_be_eligible == Time.ONE_YEARS_FROM_NOW

    def test_mrd_does_not_block_convictions(self):
        case = CaseFactory.create()
        convicted_charge = ChargeFactory.create(
            case_number=case.case_number,
            date=Time.TWENTY_YEARS_AGO,
            disposition=Disposition(ruling="Convicted", date=Time.TWENTY_YEARS_AGO),
            violation_type=case.violation_type,
        )
        case.charges = [convicted_charge]

        record = Record([self.case_1, case])
        expunger = Expunger(record)
        expunger_result = expunger.run()

        assert expunger_result[convicted_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[convicted_charge.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[
            convicted_charge.ambiguous_charge_id
        ].date_will_be_eligible == convicted_charge.disposition.date + relativedelta(years=+3)


class TestSecondMRCLogic(unittest.TestCase):
    def run_expunger(self, mrc, second_mrc):
        case = CaseFactory.create()
        case.charges = [mrc, second_mrc]
        record = Record([case])
        expunger = Expunger(record)
        return expunger.run()

    def test_3_yr_old_conviction_2_yr_old_mrc(self):
        three_years_ago_charge = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.THREE_YEARS_AGO)
        )
        two_years_ago_charge = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.TWO_YEARS_AGO)
        )

        expunger_result = self.run_expunger(two_years_ago_charge, three_years_ago_charge)

        assert expunger_result[three_years_ago_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[three_years_ago_charge.ambiguous_charge_id].reason
            == "Ten years from most recent other conviction (137.225(7)(b))"
        )
        assert (
            expunger_result[three_years_ago_charge.ambiguous_charge_id].date_will_be_eligible
            == two_years_ago_charge.disposition.date + Time.TEN_YEARS
        )

        assert expunger_result[two_years_ago_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[two_years_ago_charge.ambiguous_charge_id].reason
            == "Ten years from most recent other conviction (137.225(7)(b))"
        )
        assert (
            expunger_result[two_years_ago_charge.ambiguous_charge_id].date_will_be_eligible
            == three_years_ago_charge.disposition.date + Time.TEN_YEARS
        )

    def test_7_yr_old_conviction_5_yr_old_mrc(self):
        seven_year_ago_charge = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.SEVEN_YEARS_AGO)
        )
        five_year_ago_charge = ChargeFactory.create(
            disposition=Disposition(ruling="Convicted", date=Time.FIVE_YEARS_AGO)
        )

        expunger_result = self.run_expunger(five_year_ago_charge, seven_year_ago_charge)

        assert expunger_result[seven_year_ago_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[seven_year_ago_charge.ambiguous_charge_id].reason
            == "Ten years from most recent other conviction (137.225(7)(b))"
        )
        assert (
            expunger_result[seven_year_ago_charge.ambiguous_charge_id].date_will_be_eligible
            == five_year_ago_charge.disposition.date + Time.TEN_YEARS
        )

        assert expunger_result[five_year_ago_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[five_year_ago_charge.ambiguous_charge_id].reason
            == "Ten years from most recent other conviction (137.225(7)(b))"
        )
        assert (
            expunger_result[five_year_ago_charge.ambiguous_charge_id].date_will_be_eligible
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

        expunger_result = self.run_expunger(one_year_old_conviction, nine_year_old_conviction)

        assert expunger_result[one_year_old_conviction.ambiguous_charge_id].date_will_be_eligible == eligibility_date


def create_class_b_felony_charge(case, date, ruling="Convicted"):
    return ChargeFactory.create(
        case_number=case.case_number,
        name="Aggravated theft in the first degree",
        statute="164.057",
        level="Felony Class B",
        date=date,
        disposition=Disposition(ruling=ruling, date=date),
        violation_type=case.violation_type,
    )


def test_felony_class_b_greater_than_20yrs():
    case = CaseFactory.create()
    charge = create_class_b_felony_charge(case, Time.TWENTY_YEARS_AGO)
    case.charges = [charge]
    expunger = Expunger(Record([case]))
    expunger_result = expunger.run()

    assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[charge.ambiguous_charge_id].reason == "Eligible now"
    assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible == date.today()


def test_felony_class_b_less_than_20yrs():
    case = CaseFactory.create()
    charge = create_class_b_felony_charge(case, Time.LESS_THAN_TWENTY_YEARS_AGO)
    case.charges = [charge]
    expunger = Expunger(Record([case]))
    expunger_result = expunger.run()

    assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[charge.ambiguous_charge_id].reason
        == "Twenty years from date of class B felony conviction (137.225(5)(a)(A)(i))"
    )
    assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible == Time.TOMORROW


def test_felony_class_b_with_subsequent_conviction():
    case_1 = CaseFactory.create(case_number="1")
    b_felony_charge = create_class_b_felony_charge(case_1, Time.TWENTY_YEARS_AGO)
    case_1.charges = [b_felony_charge]
    subsequent_charge = ChargeFactory.create(disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO))
    case_2 = CaseFactory.create(case_number="2")
    case_2.charges = [subsequent_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger_result = expunger.run()

    assert expunger_result[b_felony_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[b_felony_charge.ambiguous_charge_id].reason
        == "Never. Class B felony can have no subsequent arrests or convictions (137.225(5)(a)(A)(ii))"
    )
    assert expunger_result[b_felony_charge.ambiguous_charge_id].date_will_be_eligible == date.max

    # The Class B felony does not affect eligibility of another charge that is otherwise eligible
    assert expunger_result[subsequent_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert subsequent_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE


def test_felony_class_b_with_prior_conviction():
    case_1 = CaseFactory.create(case_number="1")
    b_felony_charge = create_class_b_felony_charge(case_1, Time.TWENTY_YEARS_AGO)
    case_1.charges = [b_felony_charge]
    prior_charge = ChargeFactory.create(
        disposition=Disposition(ruling="Convicted", date=Time.MORE_THAN_TWENTY_YEARS_AGO)
    )
    case_2 = CaseFactory.create(case_number="2")
    case_2.charges = [prior_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger_result = expunger.run()

    assert b_felony_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        b_felony_charge.type_eligibility.reason
        == "Convictions that fulfill the conditions of 137.225(5)(a) are eligible"
    )
    assert expunger_result[b_felony_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[b_felony_charge.ambiguous_charge_id].reason == "Eligible now"


def test_dismissed_felony_class_b_with_subsequent_conviction():
    case_1 = CaseFactory.create(case_number="1")
    b_felony_charge = create_class_b_felony_charge(case_1, Time.LESS_THAN_TWENTY_YEARS_AGO, "Dismissed")
    case_1.charges = [b_felony_charge]
    case_2 = CaseFactory.create(case_number="2")
    subsequent_charge = ChargeFactory.create(
        case_number=case_2.case_number,
        disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO),
        violation_type=case_2.violation_type,
    )
    case_2.charges = [subsequent_charge]

    expunger = Expunger(Record([case_1, case_2]))
    expunger_result = expunger.run()

    assert b_felony_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert expunger_result[b_felony_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE


def test_doubly_eligible_b_felony_gets_normal_eligibility_rule():
    # This charge is both ManufactureDelivery and also a class B felony. ManufactureDelivery classification takes precedence and the B felony time rule does not apply.
    manudel_charges = ChargeFactory.create_ambiguous_charge(
        case_number="1",
        name="Manufacture/Delivery 1",
        statute="4759922b",
        level="Felony Class B",
        date=Time.LESS_THAN_TWENTY_YEARS_AGO,
        disposition=Disposition(ruling="Convicted", date=Time.LESS_THAN_TWENTY_YEARS_AGO),
    )
    manudel_type_eligilibility = RecordMerger.merge_type_eligibilities(manudel_charges)

    case_1a = CaseFactory.create(case_number="1")
    case_1a.charges = [manudel_charges[0]]
    case_1b = CaseFactory.create(case_number="1")
    case_1b.charges = [manudel_charges[1]]
    case_2 = CaseFactory.create(case_number="2")
    subsequent_charge = ChargeFactory.create(
        case_number=case_2.case_number, disposition=Disposition(ruling="Convicted", date=Time.TEN_YEARS_AGO)
    )
    case_2.charges = [subsequent_charge]

    possible_record_1 = Record([case_1a, case_2])
    possible_record_2 = Record([case_1b, case_2])
    expunger = Expunger(possible_record_1)
    expunger_result_1 = expunger.run()
    expunger = Expunger(possible_record_2)
    expunger_result_2 = expunger.run()

    assert manudel_type_eligilibility.status is EligibilityStatus.ELIGIBLE
    assert expunger_result_1[manudel_charges[0].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result_2[manudel_charges[1].ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE


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
    expunger_result = expunger.run()

    assert expunger_result[violation_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[violation_charge.ambiguous_charge_id].reason
        == "Three years from date of conviction (137.225(1)(a))"
    )
    assert expunger_result[violation_charge.ambiguous_charge_id].date_will_be_eligible == date.today() + relativedelta(
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
    expunger_result = expunger.run()

    assert expunger_result[violation_charge_1.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[violation_charge_1.ambiguous_charge_id].reason
        == "Three years from date of conviction (137.225(1)(a))"
    )
    assert (
        expunger_result[violation_charge_1.ambiguous_charge_id].date_will_be_eligible
        == violation_charge_1.disposition.date + Time.THREE_YEARS
    )

    assert expunger_result[violation_charge_2.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[violation_charge_2.ambiguous_charge_id].reason
        == "Three years from date of conviction (137.225(1)(a))"
    )
    assert (
        expunger_result[violation_charge_2.ambiguous_charge_id].date_will_be_eligible
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
    expunger_result = expunger.run()

    assert expunger_result[violation_charge_1.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[violation_charge_1.ambiguous_charge_id].reason
        == "Ten years from most recent other conviction (137.225(7)(b))"
    )
    assert (
        expunger_result[violation_charge_1.ambiguous_charge_id].date_will_be_eligible
        == violation_charge_2.disposition.date + Time.TEN_YEARS
    )

    assert expunger_result[violation_charge_2.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[violation_charge_2.ambiguous_charge_id].reason
        == "Ten years from most recent other conviction (137.225(7)(b))"
    )
    assert (
        expunger_result[violation_charge_2.ambiguous_charge_id].date_will_be_eligible
        == violation_charge_1.disposition.date + Time.TEN_YEARS
    )

    assert expunger_result[violation_charge_3.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[violation_charge_3.ambiguous_charge_id].reason
        == "Ten years from most recent other conviction (137.225(7)(b))"
    )
    assert (
        expunger_result[violation_charge_3.ambiguous_charge_id].date_will_be_eligible
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
    expunger_result = expunger.run()

    assert expunger_result[civil_offense.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[civil_offense.ambiguous_charge_id].reason
        == "Never. Type ineligible charges are always time ineligible."
    )
    assert expunger_result[civil_offense.ambiguous_charge_id].date_will_be_eligible == date.max

    assert expunger_result[violation_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
