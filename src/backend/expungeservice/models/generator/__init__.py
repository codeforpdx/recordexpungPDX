from _weakref import ref

from hypothesis._strategies import none, composite

from expungeservice.expunger.expunger import Expunger
from expungeservice.models.case import Case
from expungeservice.models.record import Record
from hypothesis.strategies import builds, just, lists, one_of

from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge
from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.level_800_traffic_crime import Level800TrafficCrime
from expungeservice.models.charge_types.list_b import ListB
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.charge_types.non_traffic_violation import NonTrafficViolation
from expungeservice.models.charge_types.parking_ticket import ParkingTicket
from expungeservice.models.charge_types.person_crime import PersonCrime
from expungeservice.models.charge_types.schedule_1_p_c_s import Schedule1PCS
from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge

charge_types = [JuvenileCharge, FelonyClassA, FelonyClassB, FelonyClassC, Level800TrafficCrime, ListB, MarijuanaIneligible, Misdemeanor, NonTrafficViolation, ParkingTicket, PersonCrime, Schedule1PCS, UnclassifiedCharge]

@composite
def _build_case_strategy(draw, min_charges_size=0):
    case = draw(builds(Case, charges=none()))
    charge_strategy_choices = list(map(lambda charge_type: builds(charge_type, _case=just(ref(case))), charge_types))
    charge_strategy = one_of(charge_strategy_choices)
    charges = draw(lists(charge_strategy, min_charges_size))
    case.charges = charges
    return case

def build_record_strategy(min_cases_size=0, min_charges_size=0):
    case_strategy = _build_case_strategy(min_charges_size)
    return builds(Record, cases=lists(case_strategy, min_cases_size))


def build_record():
    record_strategy = build_record_strategy(min_cases_size=10, min_charges_size=1)
    record = record_strategy.example()
    expunger = Expunger(record)
    expunger.run()
    return record