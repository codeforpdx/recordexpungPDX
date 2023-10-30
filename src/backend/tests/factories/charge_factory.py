from expungeservice.util import DateWithFuture as date_class
from expungeservice.models.ambiguous import AmbiguousCharge
from expungeservice.models.charge import Charge, EditStatus
from expungeservice.charge_creator import ChargeCreator
from expungeservice.models.disposition import Disposition, DispositionCreator, DispositionStatus


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
        disposition: Disposition = DispositionCreator.empty(),
        violation_type="Offense Misdemeanor",
        location="Benton"
    ) -> Charge:
        charges = cls._build_ambiguous_charge(case_number, date, disposition, level, name, statute, violation_type, location)
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
        disposition: Disposition = DispositionCreator.empty(),
        violation_type="Offense Misdemeanor",
        location="Benton"
    ) -> AmbiguousCharge:
        return cls._build_ambiguous_charge(case_number, date, disposition, level, name, statute, violation_type, location)

    @classmethod
    def _build_ambiguous_charge(cls, case_number, date, disposition, level, name, statute, violation_type, location):
        cls.charge_count += 1
        if disposition.status != DispositionStatus.UNKNOWN and not date:
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
            "location": location,
            "balance_due_in_cents": 0,
            "edit_status": EditStatus.UNCHANGED,
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
        location="Benton"
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
            "location": location,
            "balance_due_in_cents": 0,
            "edit_status": EditStatus.UNCHANGED,
        }

        charges = ChargeCreator.create(str(cls.charge_count), **kwargs)[0]
        assert len(charges) == 1
        return charges[0]
