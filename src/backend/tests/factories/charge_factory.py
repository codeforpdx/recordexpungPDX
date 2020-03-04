from datetime import date as date_class
from expungeservice.models.helpers.charge_creator import ChargeCreator
from expungeservice.models.disposition import Disposition
from tests.factories.case_factory import CaseFactory


class ChargeFactory:
    charge_count = 0  # Responsible for giving every Charge in tests an unique deterministic ID

    @classmethod
    def create(
        cls,
        case=CaseFactory.create(),
        name="Theft of services",
        statute="164.125",
        level="Misdemeanor Class A",
        date: date_class = None,
        disposition: Disposition = None,
    ):
        cls.charge_count += 1
        if disposition and not date:
            date_string = disposition.date.strftime("%m/%d/%Y")
        elif date:
            date_string = date.strftime("%m/%d/%Y")
        else:
            date_string = "1/1/1901"
        kwargs = {
            "case": case,
            "name": name,
            "statute": statute,
            "level": level,
            "date": date_string,
            "disposition": disposition,
        }

        return ChargeCreator.create(cls.charge_count, **kwargs)

    @classmethod
    def create_dismissed_charge(
        cls,
        case=CaseFactory.create(),
        name="Theft of services",
        statute="164.125",
        level="Misdemeanor Class A",
        date=date_class(1901, 1, 1),
    ):
        cls.charge_count += 1
        disposition = Disposition(date=date_class.today(), ruling="Dismissed")
        kwargs = {
            "case": case,
            "name": name,
            "statute": statute,
            "level": level,
            "date": date.strftime("%m/%d/%Y"),
            "disposition": disposition,
        }

        return ChargeCreator.create(cls.charge_count, **kwargs)
