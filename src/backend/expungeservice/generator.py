import pkgutil
from dataclasses import replace
from datetime import date
from typing import List, Type, Callable, Any

from hypothesis._strategies import none, composite, dates
from hypothesis.strategies import builds, just, lists, one_of
from hypothesis.searchstrategy import SearchStrategy

from expungeservice.models.case import Case, CaseSummary
from expungeservice.models.charge_types.dismissed_charge import DismissedCharge
from expungeservice.models.disposition import DispositionStatus, Disposition
from expungeservice.models.record import Record

from importlib import import_module
from expungeservice.models.charge import Charge, ChargeType
from expungeservice.models import charge_types
import inspect
from expungeservice.util import DateWithFuture


def _is_proper_charge_subclass(attr):
    return inspect.isclass(attr) and issubclass(attr, ChargeType) and attr != ChargeType


def get_charge_classes() -> List[Type[ChargeType]]:
    charge_classes: List[Type[ChargeType]] = []
    for _, module_name, _ in pkgutil.iter_modules(charge_types.__path__):  # type: ignore  # mypy issue #1422
        module = import_module(f"{charge_types.__name__}.{module_name}")
        attrs = list(module.__dict__.values())
        charge_subclass_attrs = list(filter(lambda attr: _is_proper_charge_subclass(attr), attrs))
        charge_classes += charge_subclass_attrs
    return charge_classes


@composite
def _build_charge_strategy(
    draw: Callable[[SearchStrategy], Any], charge_type: ChargeType, case: CaseSummary
) -> SearchStrategy[Charge]:
    if charge_type == DismissedCharge():
        disposition_status = one_of(
            just(DispositionStatus.DISMISSED), just(DispositionStatus.NO_COMPLAINT), just(DispositionStatus.DIVERTED)
        )
    else:
        disposition_status = one_of(just(DispositionStatus.CONVICTED), just(DispositionStatus.UNRECOGNIZED))
    disposition_date = just(DateWithFuture(date=draw(dates(max_value=date(9000, 12, 31)))))
    disposition = builds(Disposition, status=disposition_status, date=disposition_date)
    arrest_date = just(DateWithFuture(date=draw(dates(max_value=date(9000, 12, 31)))))
    probation_revoked_date = one_of(none(), just(DateWithFuture(date=draw(dates(max_value=date(9000, 12, 31))))))
    return draw(
        builds(
            Charge,
            charge_type=just(charge_type),
            case_number=just(case.case_number),
            disposition=disposition,
            date=arrest_date,
            probation_revoked=probation_revoked_date,
        )
    )


@composite
def _build_case_strategy(draw: Callable[[SearchStrategy], Any], min_charges_size=0) -> Case:
    case_summary = draw(builds(CaseSummary, date=just(DateWithFuture(date=draw(dates())))))
    charge_classes = get_charge_classes()
    charge_strategy_choices = list(
        map(lambda charge_class: _build_charge_strategy(charge_class(), case_summary), charge_classes)
    )
    charge_strategy = one_of(charge_strategy_choices)
    charges = draw(lists(charge_strategy, min_charges_size))
    return Case(case_summary, charges=tuple(charges))


@composite
def build_record_strategy(draw: Callable[[SearchStrategy], Any], min_cases_size=0, min_charges_size=0) -> Record:
    case_strategy = _build_case_strategy(min_charges_size)
    cases = draw(lists(case_strategy, min_cases_size))
    record = draw(builds(Record, cases=none()))
    return replace(record, cases=tuple(cases))


def build_record() -> Record:
    return build_record_strategy(min_cases_size=10, min_charges_size=1)  # type: ignore
