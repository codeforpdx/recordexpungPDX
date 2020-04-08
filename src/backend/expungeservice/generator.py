import pkgutil
from dataclasses import replace
from typing import List, Type, Callable, Any

from hypothesis._strategies import none, composite
from hypothesis.strategies import builds, just, lists, one_of
from hypothesis.searchstrategy import SearchStrategy

from expungeservice.models.case import Case
from expungeservice.models.charge_types.dismissed_charge import DismissedCharge
from expungeservice.models.disposition import DispositionStatus, Disposition
from expungeservice.models.record import Record

from importlib import import_module
from expungeservice.models.charge import Charge
from expungeservice.models import charge_types
import inspect


def _is_proper_charge_subclass(attr):
    return inspect.isclass(attr) and issubclass(attr, Charge) and attr != Charge


def get_charge_classes() -> List[Type[Charge]]:
    charge_classes: List[Type[Charge]] = []
    for _, module_name, _ in pkgutil.iter_modules(charge_types.__path__):  # type: ignore  # mypy issue #1422
        module = import_module(f"{charge_types.__name__}.{module_name}")
        attrs = list(module.__dict__.values())
        charge_subclass_attrs = list(filter(lambda attr: _is_proper_charge_subclass(attr), attrs))
        charge_classes += charge_subclass_attrs
    return charge_classes


def _build_charge_strategy(charge_class: Type[Charge], case: Case) -> SearchStrategy[Charge]:
    if charge_class == DismissedCharge:
        disposition_status = one_of(
            just(DispositionStatus.DISMISSED), just(DispositionStatus.NO_COMPLAINT), just(DispositionStatus.DIVERTED)
        )
    else:
        disposition_status = one_of(just(DispositionStatus.CONVICTED), just(DispositionStatus.UNRECOGNIZED))
    disposition = builds(Disposition, status=disposition_status)
    return builds(charge_class, case_number=just(case.case_number), disposition=one_of(none(), disposition))


@composite
def _build_case_strategy(draw: Callable[[SearchStrategy], Any], min_charges_size=0) -> Case:
    case = draw(builds(Case, charges=none()))
    charge_classes = get_charge_classes()
    charge_strategy_choices = list(map(lambda charge_class: _build_charge_strategy(charge_class, case), charge_classes))
    charge_strategy = one_of(charge_strategy_choices)
    charges = draw(lists(charge_strategy, min_charges_size))
    return replace(case, charges=tuple(charges))


@composite
def build_record_strategy(draw: Callable[[SearchStrategy], Any], min_cases_size=0, min_charges_size=0) -> Record:
    case_strategy = _build_case_strategy(min_charges_size)
    cases = draw(lists(case_strategy, min_cases_size))
    record = draw(builds(Record, cases=none()))
    return replace(record, cases=tuple(cases))


def build_record() -> Record:
    return build_record_strategy(min_cases_size=10, min_charges_size=1)  # type: ignore
