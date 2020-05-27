from expungeservice.util import DateWithFuture as date

from expungeservice.models.disposition import DispositionCreator
from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.parking_ticket import ParkingTicket

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseSummaryFactory
from tests.models.test_charge import Dispositions


def test_parking_ticket_conviction():
    case = CaseSummaryFactory.create(type_status=["Municipal Parking", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Unknown",
        statute="109",
        level="Violation Unclassified",
        date=date(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge, ParkingTicket)
    assert not charge.blocks_other_charges
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible under 137.225(7)(a)"


def test_parking_ticket_dismissal():
    case = CaseSummaryFactory.create(type_status=["Municipal Parking", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Unknown",
        statute="109",
        level="Violation Unclassified",
        date=date(1901, 1, 1),
        disposition=Dispositions.DISMISSED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge, ParkingTicket)
    assert not charge.blocks_other_charges
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert charge.type_eligibility.reason == "Ineligible by omission from statute"


def test_parking_ticket_no_disposition():
    case = CaseSummaryFactory.create(type_status=["Municipal Parking", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Unknown",
        statute="109",
        level="Violation Unclassified",
        date=date(1901, 1, 1),
        disposition=DispositionCreator.empty(),
        violation_type=case.violation_type,
    )

    assert isinstance(charge, ParkingTicket)
    assert not charge.blocks_other_charges
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        charge.type_eligibility.reason
        == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
    )


def test_parking_ticket_unrecognized_disposition():
    case = CaseSummaryFactory.create(type_status=["Municipal Parking", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Unknown",
        statute="109",
        level="Violation Unclassified",
        date=date(1901, 1, 1),
        disposition=Dispositions.UNRECOGNIZED_DISPOSITION,
        violation_type=case.violation_type,
    )

    assert isinstance(charge, ParkingTicket)
    assert not charge.blocks_other_charges
    assert charge.type_eligibility.status is EligibilityStatus.INELIGIBLE
    assert (
        charge.type_eligibility.reason
        == "Always ineligible under 137.225(7)(a) (for convictions) or by omission from statute (for dismissals)"
    )
