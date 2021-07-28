from expungeservice.util import DateWithFuture as date_class
from expungeservice.models.charge_types.civil_offense import CivilOffense
from expungeservice.models.charge_types.dismissed_charge import DismissedCharge
from expungeservice.models.charge_types.duii import DivertedDuii
from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible
from expungeservice.models.charge_types.misdemeanor_class_a import MisdemeanorClassA
from expungeservice.models.charge_types.misdemeanor_class_bc import MisdemeanorClassBC
from expungeservice.models.charge_types.parking_ticket import ParkingTicket
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.models.charge_types.sex_crimes import SexCrime
from expungeservice.models.charge_types.subsection_6 import Subsection6
from expungeservice.models.charge_types.traffic_offense import TrafficOffense
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseSummaryFactory
from tests.models.test_charge import Dispositions


def test_civil_offense_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Civil Offense", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Defamation",
        statute="99",
        level="N/A",
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, CivilOffense)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_duii_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["DUII", "Closed"])
    charges = ChargeFactory.create_ambiguous_charge(
        case_number=case.case_number,
        name="Driving Under the Influence",
        statute="813.010",
        level="N/A",
        disposition=Dispositions.DISMISSED,
        violation_type=case.violation_type,
    )

    assert isinstance(charges[0].charge_type, DivertedDuii)
    assert charges[0].charge_type.hidden_in_record_summary() == False
    assert isinstance(charges[1].charge_type, DismissedCharge)
    assert charges[1].charge_type.hidden_in_record_summary() == False


def test_felony_class_a_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Offense Felony Class A", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Assault in the first degree",
        statute="163.185",
        level="Felony Class A",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, FelonyClassA)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_felony_class_b_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Offense Felony Class B", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Aggravated theft in the first degree",
        statute="164.057",
        level="Felony Class B",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, FelonyClassB)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_felony_class_c_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Offense Felony Class C", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Theft in the first degree",
        statute="164.055",
        level="Felony Class C",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, FelonyClassC)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_juvenile_charge_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Juvenile Delinquency: Misdemeanor", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Theft in the first degree",
        statute="N/A",
        level="N/A",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, JuvenileCharge)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_marijuana_eligible_hidden_in_summary():
    charge = ChargeFactory.create(
        name="Delivery of Marijuana to Minor",
        statute="4758604A",
        level="Felony Class A",
        disposition=Dispositions.DISMISSED,
    )
    assert isinstance(charge.charge_type, DismissedCharge)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_marijuana_ineligible_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Offense Felony Class C", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Unlawful Manufacture of Marijuana Item",
        statute="475B.349(3)(C)",
        level="Felony Class C",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, MarijuanaIneligible)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_misdemeanor_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Offense Misdemeanor", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Theft in the third degree",
        statute="164.043",
        level="Misdemeanor Class C",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, MisdemeanorClassBC)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_parking_ticket_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Municipal Parking", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Unknown",
        statute="109",
        level="Violation Unclassified",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, ParkingTicket)
    assert charge.charge_type.hidden_in_record_summary() == True


def test_person_felony_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Personal Felony", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Generic",
        statute="97981",
        level="Felony Class B",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, PersonFelonyClassB)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_sex_crimes_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Offense Misdemeanor", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Generic",
        statute="163365",
        level="Misdemeanor Class A",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, SexCrime)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_subsection_6_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Offense Misdemeanor", "Closed"])
    charges = ChargeFactory.create_ambiguous_charge(
        case_number=case.case_number,
        name="Criminal mistreatment in the second degree",
        statute="163.200",
        level="Misdemeanor Class A",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charges[0].charge_type, Subsection6)
    assert charges[0].charge_type.hidden_in_record_summary() == False
    assert isinstance(charges[1].charge_type, MisdemeanorClassA)
    assert charges[1].charge_type.hidden_in_record_summary() == False


def test_traffic_offense_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Traffic Offense", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="N/A",
        statute="802",
        level="felony violation",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, TrafficOffense)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_traffic_violation_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Traffic Violation", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="N/A",
        statute="801",
        level="Violation",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, TrafficViolation)
    assert charge.charge_type.hidden_in_record_summary() == True


def test_unclassified_charge_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Offense Felony", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Assault in the ninth degree",
        statute="333.333",
        level="Felony Class F",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, UnclassifiedCharge)
    assert charge.charge_type.hidden_in_record_summary() == False


def test_violation_hidden_in_summary():
    case = CaseSummaryFactory.create(type_status=["Violation", "Closed"])
    charge = ChargeFactory.create(
        case_number=case.case_number,
        name="Assault in the first degree",
        statute="333.333",
        level="Felony Class F",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.DISMISSED,
        violation_type=case.violation_type,
    )

    assert isinstance(charge.charge_type, UnclassifiedCharge)
    assert charge.charge_type.hidden_in_record_summary() == False
