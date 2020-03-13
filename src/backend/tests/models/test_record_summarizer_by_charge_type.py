from datetime import date as date_class
from expungeservice.models.charge_types.civil_offense import CivilOffense
from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt
from expungeservice.models.charge_types.duii import Duii, DivertedDuii
from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaEligible
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.charge_types.parking_ticket import ParkingTicket
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.models.charge_types.sex_crimes import SexCrime
from expungeservice.models.charge_types.subsection_6 import Subsection6
from expungeservice.models.charge_types.traffic_non_violation import TrafficNonViolation
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge
from expungeservice.models.charge_types.violation import Violation

import pytest

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseFactory
from tests.models.test_charge import Dispositions

def test_civil_offense_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Civil Offense", "Closed"]),
        name="Defamation",
        statute="99",
        level="N/A",
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, CivilOffense)
    assert charge.hidden_in_record_summary() == False

'''
def test_contempt_of_court_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Contempt of Court", "Closed"]),
        name="contempt of court",
        statute="33",
        level="N/A",
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, ContemptOfCourt)
    assert charge.hidden_in_record_summary() == False
'''

def test_duii_hidden_in_summary():
    charges = ChargeFactory.create_ambiguous_charge(
        case=CaseFactory.create(type_status=["DUII", "Closed"]),
        name="Driving Under the Influence",
        statute="813.010",
        level="N/A",
        disposition=Dispositions.DISMISSED
    )

    assert isinstance(charges[0], Duii)
    assert charges[0].hidden_in_record_summary() == False
    assert isinstance(charges[1], DivertedDuii)
    assert charges[1].hidden_in_record_summary() == False

def test_felony_class_a_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Offense Felony Class A", "Closed"]),
        name="Assault in the first degree",
        statute="163.185",
        level="Felony Class A",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, FelonyClassA)
    assert charge.hidden_in_record_summary() == False

def test_felony_class_b_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Offense Felony Class B", "Closed"]),
        name="Aggravated theft in the first degree",
        statute="164.057",
        level="Felony Class B",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, FelonyClassB)
    assert charge.hidden_in_record_summary() == False

def test_felony_class_c_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Offense Felony Class C", "Closed"]),
        name="Theft in the first degree",
        statute="164.055",
        level="Felony Class C",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, FelonyClassC)
    assert charge.hidden_in_record_summary() == False


def test_juvenile_charge_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Juvenile Delinquency: Misdemeanor", "Closed"]),
        name="Theft in the first degree",
        statute="N/A",
        level="N/A",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, JuvenileCharge)
    assert charge.hidden_in_record_summary() == False

def test_marijuana_ineligible_hidden_in_summary():
    charge = ChargeFactory.create(
        name="Delivery of Marijuana to Minor",
        statute="4758604A",
        level="Felony Class A",
        disposition=Dispositions.DISMISSED,
    )
    assert isinstance(charge, MarijuanaEligible)
    assert charge.hidden_in_record_summary() == False

def test_marijuana_ineligible_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Offense Felony Class C", "Closed"]),
        name="Unlawful Manufacture of Marijuana Item",
        statute="475B.349(3)(C)",
        level="Felony Class C",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, MarijuanaIneligible)
    assert charge.hidden_in_record_summary() == False

def test_misdemeanor_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Offense Misdemeanor", "Closed"]),
        name="Theft in the third degree",
        statute="164.043",
        level="Misdemeanor Class C",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, Misdemeanor)
    assert charge.hidden_in_record_summary() == False

def test_parking_ticket_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Municipal Parking", "Closed"]),
        name="Unkown",
        statute="109",
        level="Violation Unclassified",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, ParkingTicket)
    assert charge.hidden_in_record_summary() == True

def test_person_felony_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Personal Felony", "Closed"]),
        name="Generic",
        statute="97981",
        level="Felony Class B",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, PersonFelonyClassB)
    assert charge.hidden_in_record_summary() == False


def test_sex_crimes_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Offense Misdemeanor", "Closed"]),
        name="Generic",
        statute="163365",
        level="Misdemeanor Class A",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, SexCrime)
    assert charge.hidden_in_record_summary() == False

def test_subsection_6_hidden_in_summary():
    charges = ChargeFactory.create_ambiguous_charge(
        case=CaseFactory.create(type_status=["Offense Misdemeanor", "Closed"]),
        name="Criminal mistreatment in the second degree",
        statute="163.200",
        level="Misdemeanor Class A",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charges[0], Subsection6)
    assert charges[0].hidden_in_record_summary() == False
    assert isinstance(charges[1], Misdemeanor)
    assert charges[1].hidden_in_record_summary() == False

def test_traffic_non_violation_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Traffic Non-Violation", "Closed"]),
        name="N/A",
        statute="802",
        level="felony violation",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, TrafficNonViolation)
    assert charge.hidden_in_record_summary() == False

def test_traffic_violation_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Traffic Violation", "Closed"]),
        name="N/A",
        statute="801",
        level="Violation",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, TrafficViolation)
    assert charge.hidden_in_record_summary() == True

def test_unclassified_charge_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Offense Felony", "Closed"]),
        name="Assault in the ninth degree",
        statute="333.333",
        level="Felony Class F",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.CONVICTED
    )

    assert isinstance(charge, UnclassifiedCharge)
    assert charge.hidden_in_record_summary() == False

def test_violation_hidden_in_summary():
    charge = ChargeFactory.create(
        case=CaseFactory.create(type_status=["Violation", "Closed"]),
        name="Assault in the first degree",
        statute="333.333",
        level="Felony Class F",
        date=date_class(1901, 1, 1),
        disposition=Dispositions.DISMISSED
    )

    assert isinstance(charge, UnclassifiedCharge)
    assert charge.hidden_in_record_summary() == False
