import unittest
from dataclasses import replace

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.util import DateWithFuture as date
from dateutil.relativedelta import relativedelta

from expungeservice.charge_creator import ChargeCreator
from expungeservice.generator import get_charge_classes
from expungeservice.models.charge import ChargeType
from expungeservice.models.disposition import DispositionCreator
from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseSummaryFactory, CaseFactory
from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt
from expungeservice.models.charge_types.parking_ticket import ParkingTicket
from expungeservice.models.charge_types.traffic_violation import TrafficViolation


class Dispositions:
    LAST_WEEK = date.today() - relativedelta(days=7)
    CONVICTED = DispositionCreator.create(ruling="Convicted", date=LAST_WEEK)
    DISMISSED = DispositionCreator.create(ruling="Dismissed", date=LAST_WEEK)
    UNRECOGNIZED_DISPOSITION = DispositionCreator.create(ruling="Something unrecognized", date=LAST_WEEK)
    NO_COMPLAINT = DispositionCreator.create(ruling="No Complaint", date=LAST_WEEK)
    LESSER_CHARGE = DispositionCreator.create(ruling="Convicted - Lesser Charge", date=LAST_WEEK)


class TestChargeClass(unittest.TestCase):

    TEN_YEARS_AGO = date.today() + relativedelta(years=-10)
    LESS_THAN_TEN_YEARS_AGO = date.today() + relativedelta(years=-10, days=+1)
    LESS_THAN_THREE_YEARS_AGO = date.today() + relativedelta(years=-3, days=+1)
    THREE_YEARS_AGO = date.today() + relativedelta(years=-3)

    def test_it_initializes_simple_statute(self):
        charge = ChargeFactory.create(statute="1231235B")

        assert charge.statute == "1231235B"

    def test_it_normalizes_statute(self):
        charge = ChargeFactory.create(statute="-123.123(5)()B")

        assert charge.statute == "1231235B"

    def test_it_converts_statute_to_uppercase(self):
        charge = ChargeFactory.create(statute="-123.123(5)()b")

        assert charge.statute == "1231235B"

    def test_it_retrieves_its_parent_instance(self):
        case = CaseFactory.create()
        charge = ChargeFactory.create(case_number=case.summary.case_number)

        assert charge.case([case]) is case

    def test_it_knows_if_it_has_a_recent_conviction_happy_path(self):
        charge = ChargeFactory.create()
        charge_with_disposition = replace(
            charge, disposition=DispositionCreator.create(self.LESS_THAN_TEN_YEARS_AGO, "Convicted")
        )

        assert charge_with_disposition.recent_conviction() is True

    def test_it_knows_if_it_has_a_recent_conviction_sad_path(self):
        charge = ChargeFactory.create()
        charge_with_disposition = replace(
            charge, disposition=DispositionCreator.create(self.TEN_YEARS_AGO, "Convicted")
        )

        assert charge_with_disposition.recent_conviction() is False

    def test_dismissed_charge_is_not_a_recent_conviction(self):
        charge = ChargeFactory.create()
        charge_with_disposition = replace(
            charge, disposition=DispositionCreator.create(self.LESS_THAN_TEN_YEARS_AGO, "Dismissed")
        )

        assert charge_with_disposition.recent_conviction() is False

    def test_most_recent_dismissal_happy_path(self):
        charge = ChargeFactory.create(date=self.LESS_THAN_THREE_YEARS_AGO)
        charge_with_disposition = replace(
            charge, disposition=DispositionCreator.create(date=self.LESS_THAN_THREE_YEARS_AGO, ruling="Dismissed")
        )

        assert charge_with_disposition.recent_dismissal() is True

    def test_most_recent_dismissal_sad_path(self):
        charge = ChargeFactory.create(date=self.THREE_YEARS_AGO)
        charge_with_disposition = replace(
            charge, disposition=DispositionCreator.create(date=self.THREE_YEARS_AGO, ruling="Dismissed")
        )

        assert charge_with_disposition.recent_dismissal() is False

    def test_convicted_charge_is_not_a_recent_dismissal(self):
        charge = ChargeFactory.create(date=self.LESS_THAN_THREE_YEARS_AGO)
        charge_with_disposition = replace(
            charge, disposition=DispositionCreator.create(date=self.LESS_THAN_THREE_YEARS_AGO, ruling="Convicted")
        )

        assert charge_with_disposition.recent_dismissal() is False

    def test_same_charge_is_not_equal(self):
        case = CaseSummaryFactory.create()
        mrc_charge = ChargeFactory.create(case_number=case.case_number)
        second_mrc_charge = ChargeFactory.create(case_number=case.case_number)

        assert mrc_charge != second_mrc_charge


# TODO: Clean up testing of private methods
class TestChargeStatuteSectionAssignment(unittest.TestCase):
    def test_it_sets_section_to_the_first_6_digits_of_statute(self):
        section = ChargeCreator._set_section("1231235B")
        assert section == "123123"

    def test_it_sets_section_to_the_first_7_digits_when_4th_char_in_statute_is_a_letter(self):
        section = ChargeCreator._set_section(statute="475B3493C")
        assert section == "475B349"

    def test_it_sets_section_to_none_if_statute_is_does_not_contain_a_section(self):
        section = ChargeCreator._set_section(statute="29")
        assert section == ""

    def test_it_normalizes_section(self):
        section = ChargeCreator._set_section(statute=ChargeCreator._strip_non_alphanumeric_chars("475B.349(3)(C)"))
        assert section == "475B349"


def test_nonblocking_charges_are_never_type_eligible_except_contempt_of_court():
    for charge_class in get_charge_classes():
        if (
            not charge_class().blocks_other_charges
            and not isinstance(charge_class(), ContemptOfCourt)
            and not isinstance(charge_class(), ParkingTicket)
            and not isinstance(charge_class(), TrafficViolation)
        ):
            assert_charge_class_is_never_type_eligible(charge_class())


def assert_charge_class_is_never_type_eligible(charge_type: ChargeType):
    for disposition in [
        Dispositions.CONVICTED,
        Dispositions.DISMISSED,
        Dispositions.UNRECOGNIZED_DISPOSITION,
        Dispositions.NO_COMPLAINT,
    ]:
        type_eligibility = charge_type.type_eligibility(disposition)
        assert type_eligibility.status != EligibilityStatus.ELIGIBLE
