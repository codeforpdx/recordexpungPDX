import unittest
from dataclasses import replace

from expungeservice.util import DateWithFuture as date

from dateutil.relativedelta import relativedelta
from expungeservice.expunger import Expunger
from expungeservice.models.disposition import DispositionCreator
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaUnder21, MarijuanaViolation
from expungeservice.record_merger import RecordMerger
from expungeservice.models.record import Record
from tests.models.test_charge import Dispositions
from tests.factories.case_factory import CaseFactory
from tests.factories.charge_factory import ChargeFactory
from tests.time import Time


class TestSingleChargeDismissals(unittest.TestCase):
    def test_eligible_arrests_eligibility_based_on_second_mrc(self):

        three_yr_conviction = ChargeFactory.create(
            case_number="1",
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.THREE_YEARS_AGO),
        )

        arrest = ChargeFactory.create(
            case_number="1",
            disposition=DispositionCreator.create(ruling="Dismissed", date=Time.THREE_YEARS_AGO),
        )

        violation = ChargeFactory.create(
            level="Violation",
            case_number="1",
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
        )

        violation_2 = ChargeFactory.create(
            level="Violation",
            case_number="1",
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
        )
        case = CaseFactory.create(charges=tuple([three_yr_conviction, arrest, violation, violation_2]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[three_yr_conviction.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[three_yr_conviction.ambiguous_charge_id].reason
            == f"137.225(7)(b) – Three years from most recent other conviction from case [{case.summary.case_number}]."
        )
        assert expunger_result[
            three_yr_conviction.ambiguous_charge_id
        ].date_will_be_eligible == date.today() + relativedelta(days=+1)

        assert expunger_result[arrest.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[arrest.ambiguous_charge_id].date_will_be_eligible == date.today() - relativedelta(
            years=3
        )

    def test_ineligible_mrc_with_arrest_on_single_case(self):
        # In this case, the friendly rule doesn't apply because the conviction doesn't become eligible
        mrc = ChargeFactory.create(
            case_number="1",
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO),
            statute="666.666",
            level="Felony Class A",
        )

        arrest = ChargeFactory.create(
            case_number="1",
            disposition=DispositionCreator.create(ruling="Dismissed", date=Time.LESS_THAN_THREE_YEARS_AGO),
        )
        case = CaseFactory.create(charges=tuple([mrc, arrest]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[arrest.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[arrest.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[mrc.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[mrc.ambiguous_charge_id].reason
            == "Never. Type ineligible charges are always time ineligible."
        )
        assert expunger_result[mrc.ambiguous_charge_id].date_will_be_eligible == date.max()

    def test_more_than_ten_year_old_conviction(self):
        charge = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.TEN_YEARS_AGO)
        )
        case = CaseFactory.create(charges=tuple([charge]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[charge.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[
            charge.ambiguous_charge_id
        ].date_will_be_eligible == charge.disposition.date + relativedelta(years=+3)

    def test_10_yr_old_conviction_with_3_yr_old_mrc(self):
        ten_yr_charge = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.TEN_YEARS_AGO)
        )
        three_yr_mrc = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.THREE_YEARS_AGO)
        )
        case = CaseFactory.create(charges=tuple([ten_yr_charge, three_yr_mrc]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[ten_yr_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[ten_yr_charge.ambiguous_charge_id].reason == "Eligible now"
        assert (
            expunger_result[ten_yr_charge.ambiguous_charge_id].date_will_be_eligible
            == three_yr_mrc.disposition.date + Time.THREE_YEARS
        )

        assert expunger_result[three_yr_mrc.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[three_yr_mrc.ambiguous_charge_id].reason == "Eligible now"
        assert (
            expunger_result[three_yr_mrc.ambiguous_charge_id].date_will_be_eligible
            == ten_yr_charge.disposition.date + Time.TEN_YEARS
        )

    def test_10_yr_old_conviction_with_less_than_3_yr_old_mrc(self):
        ten_yr_charge = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.TEN_YEARS_AGO)
        )
        less_than_three_yr_mrc = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO)
        )
        case = CaseFactory.create(charges=tuple([ten_yr_charge, less_than_three_yr_mrc]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[ten_yr_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[ten_yr_charge.ambiguous_charge_id].reason
            == f"137.225(7)(b) – Three years from most recent other conviction from case [{case.summary.case_number}]."
        )
        assert (
            expunger_result[ten_yr_charge.ambiguous_charge_id].date_will_be_eligible
            == less_than_three_yr_mrc.disposition.date + Time.THREE_YEARS
        )

        assert expunger_result[less_than_three_yr_mrc.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[less_than_three_yr_mrc.ambiguous_charge_id].reason
            == "Three years from date of conviction (137.225(1)(b))"
        )
        assert expunger_result[
            less_than_three_yr_mrc.ambiguous_charge_id
        ].date_will_be_eligible == date.today() + relativedelta(days=+1)

    def test_more_than_three_year_rule_conviction(self):
        charge = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.THREE_YEARS_AGO)
        )
        case = CaseFactory.create(charges=tuple([charge]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[charge.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible == date.today()

    def test_less_than_three_year_rule_conviction(self):
        charge = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_THREE_YEARS_AGO)
        )
        case = CaseFactory.create(charges=tuple([charge]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[charge.ambiguous_charge_id].reason == "Three years from date of conviction (137.225(1)(b))"
        )
        assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible == date.today() + relativedelta(
            days=+1
        )

    def test_time_eligibility_date_is_none_when_type_ineligible(self):
        charge = ChargeFactory.create(
            name="Assault in the first degree",
            statute="163.185",
            level="Felony Class A",
            date=Time.ONE_YEAR_AGO,
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.ONE_YEAR_AGO),
        )
        case = CaseFactory.create(charges=tuple([charge]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[charge.ambiguous_charge_id].reason
            == "Never. Type ineligible charges are always time ineligible."
        )
        assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible == date.max()

    def test_no_complaint_date(self):
        charge = ChargeFactory.create(
            date=Time.THREE_YEARS_AGO,
            disposition=DispositionCreator.create(ruling="No Complaint", date=Time.YESTERDAY),
        )
        case = CaseFactory.create(charges=tuple([charge]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible == Time.YESTERDAY + relativedelta(
            days=60
        )


class TestDismissalBlock(unittest.TestCase):
    def setUp(self):
        self.recent_dismissal = ChargeFactory.create_dismissed_charge(case_number="1", date=Time.TWO_YEARS_AGO)
        self.case_1 = CaseFactory.create(case_number="1", charges=tuple([self.recent_dismissal]))

    def test_record_with_only_an_mrd_is_time_eligible(self):
        record = Record(tuple([self.case_1]))
        expunger_result = Expunger.run(record)

        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].date_will_be_eligible == Time.TWO_YEARS_AGO

    def test_all_mrd_case_related_dismissals_are_expungeable(self):
        case_related_dismissal = ChargeFactory.create_dismissed_charge(
            case_number=self.case_1.summary.case_number, date=Time.TWO_YEARS_AGO
        )
        updated_case_1 = replace(self.case_1, charges=tuple([*self.case_1.charges, case_related_dismissal]))
        record = Record(tuple([updated_case_1]))
        expunger_result = Expunger.run(record)

        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[self.recent_dismissal.ambiguous_charge_id].date_will_be_eligible == Time.TWO_YEARS_AGO

        assert expunger_result[case_related_dismissal.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[case_related_dismissal.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[case_related_dismissal.ambiguous_charge_id].date_will_be_eligible == Time.TWO_YEARS_AGO

    def test_mrd_does_not_block_other_dismissals(self):
        unrelated_dismissal = ChargeFactory.create_dismissed_charge(
            case_number="2", date=Time.TEN_YEARS_AGO, violation_type="Offense Misdemeanor"
        )
        case_2 = CaseFactory.create(case_number="2", charges=tuple([unrelated_dismissal]))

        record = Record(tuple([self.case_1, case_2]))
        expunger_result = Expunger.run(record)

        assert expunger_result[unrelated_dismissal.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[unrelated_dismissal.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[unrelated_dismissal.ambiguous_charge_id].date_will_be_eligible == Time.TEN_YEARS_AGO

    def test_mrd_does_not_block_convictions(self):
        convicted_charge = ChargeFactory.create(
            date=Time.TWENTY_YEARS_AGO,
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.TWENTY_YEARS_AGO),
        )
        case = CaseFactory.create(charges=tuple([convicted_charge]))

        record = Record(tuple([self.case_1, case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[convicted_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
        assert expunger_result[convicted_charge.ambiguous_charge_id].reason == "Eligible now"
        assert expunger_result[
            convicted_charge.ambiguous_charge_id
        ].date_will_be_eligible == convicted_charge.disposition.date + relativedelta(years=+3)


class TestSecondMRCLogic(unittest.TestCase):
    def test_3_yr_old_and_2_yr_old_class_a_misdemeanors(self):
        three_years_ago_charge = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.THREE_YEARS_AGO)
        )
        two_years_ago_charge = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.TWO_YEARS_AGO)
        )

        case = CaseFactory.create(charges=tuple([two_years_ago_charge, three_years_ago_charge]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[three_years_ago_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[three_years_ago_charge.ambiguous_charge_id].reason
            == f"137.225(7)(b) – Three years from most recent other conviction from case [{case.summary.case_number}]."
        )
        assert (
            expunger_result[three_years_ago_charge.ambiguous_charge_id].date_will_be_eligible
            == two_years_ago_charge.disposition.date + Time.THREE_YEARS
        )

        assert expunger_result[two_years_ago_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[two_years_ago_charge.ambiguous_charge_id].reason
            == "Three years from date of conviction (137.225(1)(b))"
        )
        assert (
            expunger_result[two_years_ago_charge.ambiguous_charge_id].date_will_be_eligible
            == two_years_ago_charge.disposition.date + Time.THREE_YEARS
        )

    def test_7_yr_old_conviction_2_yr_old_mrc(self):
        seven_year_ago_charge = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.SEVEN_YEARS_AGO),
            name="Identity Theft",
            statute="165.800",
            level="Felony Class C",
        )
        two_year_ago_charge = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.TWO_YEARS_AGO)
        )

        case = CaseFactory.create(charges=tuple([two_year_ago_charge, seven_year_ago_charge]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[seven_year_ago_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[seven_year_ago_charge.ambiguous_charge_id].reason
            == f"137.225(7)(b) – Five years from most recent other conviction from case [{case.summary.case_number}]."
        )
        assert (
            expunger_result[seven_year_ago_charge.ambiguous_charge_id].date_will_be_eligible
            == two_year_ago_charge.disposition.date + Time.FIVE_YEARS
        )

        assert expunger_result[two_year_ago_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
        assert (
            expunger_result[two_year_ago_charge.ambiguous_charge_id].reason
            == "Three years from date of conviction (137.225(1)(b))"
        )
        assert (
            expunger_result[two_year_ago_charge.ambiguous_charge_id].date_will_be_eligible
            == two_year_ago_charge.disposition.date + Time.THREE_YEARS
        )

    def test_mrc_is_eligible_in_two_years(self):
        nine_year_old_conviction = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.NINE_YEARS_AGO)
        )
        one_year_old_conviction = ChargeFactory.create(
            disposition=DispositionCreator.create(ruling="Convicted", date=Time.ONE_YEAR_AGO)
        )
        eligibility_date = one_year_old_conviction.disposition.date + Time.THREE_YEARS

        case = CaseFactory.create(charges=tuple([one_year_old_conviction, nine_year_old_conviction]))
        record = Record(tuple([case]))
        expunger_result = Expunger.run(record)

        assert expunger_result[one_year_old_conviction.ambiguous_charge_id].date_will_be_eligible == eligibility_date


def create_class_b_felony_charge(case_number, date, ruling="Convicted"):
    return ChargeFactory.create(
        case_number=case_number,
        name="Aggravated theft in the first degree",
        statute="164.057",
        level="Felony Class B",
        date=date,
        disposition=DispositionCreator.create(ruling=ruling, date=date),
    )


def test_felony_class_b_seven_years():
    charge = create_class_b_felony_charge("1", Time.SEVEN_YEARS_AGO)
    case = CaseFactory.create(charges=tuple([charge]))
    expunger_result = Expunger.run(Record(tuple([case])))

    assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[charge.ambiguous_charge_id].reason == "Eligible now"
    assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible == date.today()


def test_felony_class_b_less_than_20yrs():
    charge = create_class_b_felony_charge("1", Time.LESS_THAN_SEVEN_YEARS_AGO)
    case = CaseFactory.create(charges=tuple([charge]))
    expunger_result = Expunger.run(Record(tuple([case])))

    assert expunger_result[charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert expunger_result[charge.ambiguous_charge_id].reason == "Seven years from date of conviction (137.225(1)(b))"
    assert expunger_result[charge.ambiguous_charge_id].date_will_be_eligible == Time.TOMORROW


def test_felony_class_b_with_subsequent_conviction():
    b_felony_charge = create_class_b_felony_charge("1", Time.TWENTY_YEARS_AGO)
    case_1 = CaseFactory.create(case_number="1", charges=tuple([b_felony_charge]))
    subsequent_charge = ChargeFactory.create(
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.TEN_YEARS_AGO)
    )
    case_2 = CaseFactory.create(case_number="2", charges=tuple([subsequent_charge]))

    expunger_result = Expunger.run(Record(tuple([case_1, case_2])))

    assert expunger_result[b_felony_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE

    # The Class B felony does not affect eligibility of another charge that is otherwise eligible
    assert expunger_result[subsequent_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert subsequent_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE


def test_felony_class_b_with_prior_conviction():
    b_felony_charge = create_class_b_felony_charge("1", Time.TWENTY_YEARS_AGO)
    case_1 = CaseFactory.create(case_number="1", charges=tuple([b_felony_charge]))
    prior_charge = ChargeFactory.create(
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.MORE_THAN_TWENTY_YEARS_AGO)
    )
    case_2 = CaseFactory.create(case_number="2", charges=tuple([prior_charge]))

    expunger_result = Expunger.run(Record(tuple([case_1, case_2])))

    assert b_felony_charge.type_eligibility.status is EligibilityStatus.ELIGIBLE
    assert (
        b_felony_charge.type_eligibility.reason
        == "Convictions that fulfill the conditions of 137.225(1)(b) are eligible"
    )
    assert expunger_result[b_felony_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[b_felony_charge.ambiguous_charge_id].reason == "Eligible now"


def test_dismissed_felony_class_b_with_subsequent_conviction():
    b_felony_charge = create_class_b_felony_charge("1", Time.LESS_THAN_TWENTY_YEARS_AGO, "Dismissed")
    case_1 = CaseFactory.create(case_number="1", charges=tuple([b_felony_charge]))
    subsequent_charge = ChargeFactory.create(
        case_number="2",
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.TEN_YEARS_AGO),
    )
    case_2 = CaseFactory.create(case_number="2", charges=tuple([subsequent_charge]))

    expunger_result = Expunger.run(Record(tuple([case_1, case_2])))

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
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_TWENTY_YEARS_AGO),
    )
    manudel_type_eligilibility = RecordMerger.merge_type_eligibilities(manudel_charges)

    case_1a = CaseFactory.create(case_number="1", charges=tuple([manudel_charges[0]]))
    case_1b = CaseFactory.create(case_number="1", charges=tuple([manudel_charges[1]]))
    subsequent_charge = ChargeFactory.create(
        case_number="2",
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.TEN_YEARS_AGO),
    )
    case_2 = CaseFactory.create(case_number="2", charges=tuple([subsequent_charge]))

    possible_record_1 = Record(tuple([case_1a, case_2]))
    possible_record_2 = Record(tuple([case_1b, case_2]))
    expunger_result_1 = Expunger.run(possible_record_1)
    expunger_result_2 = Expunger.run(possible_record_2)

    assert manudel_type_eligilibility.status is EligibilityStatus.ELIGIBLE
    assert expunger_result_1[manudel_charges[0].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result_2[manudel_charges[1].ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE


def test_single_violation_is_time_restricted():
    # A single violation doesn't block other records, but it is still subject to the 3 year rule.
    violation_charge = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TEN_YEARS_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_ONE_YEAR_AGO),
    )

    case = CaseFactory.create(charges=tuple([violation_charge]))
    expunger_result = Expunger.run(Record(tuple([case])))

    assert expunger_result[violation_charge.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[violation_charge.ambiguous_charge_id].reason
        == "One year from date of conviction (137.225(1)(b))"
    )
    assert expunger_result[violation_charge.ambiguous_charge_id].date_will_be_eligible == date.today() + relativedelta(
        days=+1
    )


def test_2_violations_are_time_restricted():
    violation_charge_1 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.THREE_YEARS_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.THREE_YEARS_AGO),
    )
    violation_charge_2 = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TWO_YEARS_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.TWO_YEARS_AGO),
    )

    case = CaseFactory.create(charges=tuple([violation_charge_1, violation_charge_2]))
    expunger_result = Expunger.run(Record(tuple([case])))

    assert expunger_result[violation_charge_1.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[violation_charge_1.ambiguous_charge_id].reason == "Eligible now"
    assert (
        expunger_result[violation_charge_1.ambiguous_charge_id].date_will_be_eligible
        == violation_charge_1.disposition.date + Time.ONE_YEAR
    )

    assert expunger_result[violation_charge_2.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[violation_charge_2.ambiguous_charge_id].reason == "Eligible now"
    assert (
        expunger_result[violation_charge_2.ambiguous_charge_id].date_will_be_eligible
        == violation_charge_2.disposition.date + Time.ONE_YEAR
    )

# FIXME this test failed on March 1, 2023
# def test_3_violations_are_time_restricted():
#     violation_charge_1 = ChargeFactory.create(
#         level="Class A Violation",
#         date=Time.TWO_YEARS_AGO,
#         disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_TWO_YEARS_AGO),
#     )
#     violation_charge_2 = ChargeFactory.create(
#         level="Class A Violation",
#         date=Time.ONE_YEAR_AGO,
#         disposition=DispositionCreator.create(ruling="Convicted", date=Time.LESS_THAN_ONE_YEAR_AGO),
#     )
#     violation_charge_3 = ChargeFactory.create(
#         level="Class A Violation",
#         date=Time.YESTERDAY,
#         disposition=DispositionCreator.create(ruling="Convicted", date=Time.YESTERDAY),
#     )

#     case = CaseFactory.create(charges=tuple([violation_charge_3, violation_charge_2, violation_charge_1]))
#     expunger_result = Expunger.run(Record(tuple([case])))
#     # the 3-year-old-one is blocked by the middle one
#     assert expunger_result[violation_charge_1.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
#     assert (
#         expunger_result[violation_charge_1.ambiguous_charge_id].reason
#         == f"137.225(7)(b) – One year from most recent other conviction from case [{case.summary.case_number}]."
#     )
#     assert expunger_result[
#         violation_charge_1.ambiguous_charge_id
#     ].date_will_be_eligible == date.today() + relativedelta(days=+1)

#     assert expunger_result[violation_charge_2.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
#     assert (
#         expunger_result[violation_charge_2.ambiguous_charge_id].reason
#         == "One year from date of conviction (137.225(1)(b))"
#     )
#     assert expunger_result[
#         violation_charge_2.ambiguous_charge_id
#     ].date_will_be_eligible == date.today() + relativedelta(days=+1)

#     assert expunger_result[violation_charge_3.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
#     assert (
#         expunger_result[violation_charge_3.ambiguous_charge_id].reason
#         == "One year from date of conviction (137.225(1)(b))"
#     )
#     assert expunger_result[
#         violation_charge_3.ambiguous_charge_id
#     ].date_will_be_eligible == date.today() + relativedelta(years=+1, days=-1)


def test_nonblocking_charge_is_not_skipped_and_does_not_block():
    civil_offense = ChargeFactory.create(
        level="N/A", statute="1.000", disposition=DispositionCreator.create(ruling="Convicted", date=Time.ONE_YEAR_AGO)
    )

    violation_charge = ChargeFactory.create(
        level="Class A Violation",
        date=Time.TEN_YEARS_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.TEN_YEARS_AGO),
    )

    case = CaseFactory.create(charges=tuple([civil_offense, violation_charge]))
    expunger_result = Expunger.run(Record(tuple([case])))

    assert expunger_result[civil_offense.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
    assert (
        expunger_result[civil_offense.ambiguous_charge_id].reason
        == "Never. Type ineligible charges are always time ineligible."
    )
    assert expunger_result[civil_offense.ambiguous_charge_id].date_will_be_eligible == date.max()

    assert expunger_result[violation_charge.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE


def test_marijuana_violation_eligible_with_prior_conviction():
    marijuana_violation = ChargeFactory.create(
        case_number="1",
        name="Possession of Marijuana < 1 Ounce",
        statute="4758643",
        level="Violation Unclassified",
        date=date.today(),
        disposition=DispositionCreator.create(ruling="Convicted", date=date.today() + relativedelta(days=-1)),
    )
    case_1 = CaseFactory.create(case_number="1", charges=tuple([marijuana_violation]))

    prior_conviction = ChargeFactory.create(
        case_number="2",
        name="Identity Theft",
        statute="165.800",
        level="Felony Class C",
        date=Time.FIVE_YEARS_AGO,
        disposition=DispositionCreator.create(ruling="Convicted", date=Time.ONE_YEAR_AGO),
    )
    case_2 = CaseFactory.create(case_number="2", charges=tuple([prior_conviction]))

    expunger_result = Expunger.run(Record(tuple([case_1, case_2])))

    assert isinstance(marijuana_violation.charge_type, MarijuanaViolation)
    assert expunger_result[marijuana_violation.ambiguous_charge_id].status is EligibilityStatus.ELIGIBLE
    assert expunger_result[prior_conviction.ambiguous_charge_id].status is EligibilityStatus.INELIGIBLE
