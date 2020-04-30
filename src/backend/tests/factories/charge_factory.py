from datetime import date as date_class

from expungeservice.models.ambiguous import AmbiguousCharge
from expungeservice.models.charge import Charge
from expungeservice.charge_creator import ChargeCreator
from expungeservice.models.disposition import Disposition, DispositionCreator


class ChargeFactory:
    charge_count = 0  # Responsible for giving every Charge in tests an unique deterministic ID

    @classmethod
    def create(
        cls,
        case_number="1",
        name="Theft of services",
        statute="164.125",
        level="Misdemeanor Class A",
        date: date_class = None,
        disposition: Disposition = None,
        violation_type="Offense Misdemeanor",
    ) -> Charge:
        charges = cls._build_ambiguous_charge(case_number, date, disposition, level, name, statute, violation_type)
        assert len(charges) == 1
        return charges[0]

    @classmethod
    def create_ambiguous_charge(
        cls,
        case_number="1",
        name="Theft of services",
        statute="164.125",
        level="Misdemeanor Class A",
        date: date_class = None,
        disposition: Disposition = None,
        violation_type="Offense Misdemeanor",
    ) -> AmbiguousCharge:
        return cls._build_ambiguous_charge(case_number, date, disposition, level, name, statute, violation_type)

    @classmethod
    def _build_ambiguous_charge(cls, case_number, date, disposition, level, name, statute, violation_type):
        cls.charge_count += 1
        if disposition and not date:
            updated_date = disposition.date
        elif date:
            updated_date = date
        else:
            updated_date = date_class(1901, 1, 1)
        kwargs = {
            "case_number": case_number,
            "name": name,
            "statute": statute,
            "level": level,
            "date": updated_date,
            "disposition": disposition,
            "violation_type": violation_type,
        }
        charges = ChargeCreator.create(str(cls.charge_count), **kwargs)[0]
        return charges

    @classmethod
    def create_dismissed_charge(
        cls,
        case_number=1,
        name="Theft of services",
        statute="164.125",
        level="Misdemeanor Class A",
        date=date_class(1901, 1, 1),
        violation_type="Offense Misdemeanor",
    ) -> Charge:
        cls.charge_count += 1
        disposition = DispositionCreator.create(date=date_class.today(), ruling="Dismissed")
        kwargs = {
            "case_number": case_number,
            "name": name,
            "statute": statute,
            "level": level,
            "date": date,
            "disposition": disposition,
            "violation_type": violation_type,
        }

        charges = ChargeCreator.create(str(cls.charge_count), **kwargs)[0]
        assert len(charges) == 1
        return charges[0]
