import pkgutil
from _weakref import ref
from typing import List, Type, Callable, Any

from hypothesis._strategies import none, composite
from hypothesis.strategies import builds, just, lists, one_of
from hypothesis.searchstrategy import SearchStrategy

from expungeservice.expunger import Expunger
from expungeservice.models.case import Case
from expungeservice.models.record import Record

from importlib import import_module
from expungeservice.models.charge import Charge
from expungeservice.models import charge_types
import inspect


def _is_proper_charge_subclass(attr):
    return inspect.isclass(attr) and issubclass(attr, Charge) and attr != Charge


def get_charge_classes() -> List[Type[Charge]]:
    charge_classes = []
    for _, module_name, _ in pkgutil.iter_modules(charge_types.__path__):  # type: ignore  # mypy issue #1422
        module = import_module(f"{charge_types.__name__}.{module_name}")
        attrs = list(module.__dict__.values())
        charge_subclass_attrs = list(filter(lambda attr: _is_proper_charge_subclass(attr), attrs))
        assert len(charge_subclass_attrs) == 1
        charge_classes.append(charge_subclass_attrs[0])
    return charge_classes


def _build_charge_strategy(charge_class: Type[Charge], case: Case) -> SearchStrategy[Charge]:
    return builds(charge_class, _case=just(ref(case)))


@composite
def _build_case_strategy(draw: Callable[[SearchStrategy], Any], min_charges_size=0) -> Case:
    case = draw(builds(Case, charges=none()))
    charge_classes = get_charge_classes()
    charge_strategy_choices = list(map(lambda charge_class: _build_charge_strategy(charge_class, case), charge_classes))
    charge_strategy = one_of(charge_strategy_choices)
    charges = draw(lists(charge_strategy, min_charges_size))
    case.charges = charges
    return case


def build_record_strategy(min_cases_size=0, min_charges_size=0) -> SearchStrategy[Record]:
    case_strategy = _build_case_strategy(min_charges_size)
    return builds(Record, cases=lists(case_strategy, min_cases_size))


def build_record() -> Record:
    record_strategy = build_record_strategy(min_cases_size=10, min_charges_size=1)
    record = record_strategy.example()
    expunger = Expunger(record)
    expunger.run()
    return record
