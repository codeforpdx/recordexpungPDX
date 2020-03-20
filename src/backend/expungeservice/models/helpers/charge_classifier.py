from dataclasses import dataclass
from typing import List, Iterator, Type, Optional

from expungeservice.models.charge import Charge
from expungeservice.models.charge_types.dismissed_charge import DismissedCharge
from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge
from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.traffic_non_violation import TrafficNonViolation
from expungeservice.models.charge_types.duii import Duii, DivertedDuii
from expungeservice.models.charge_types.subsection_6 import Subsection6
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible
from expungeservice.models.charge_types.marijuana_eligible import MarijuanaEligible
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.charge_types.violation import Violation
from expungeservice.models.charge_types.parking_ticket import ParkingTicket
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt
from expungeservice.models.charge_types.civil_offense import CivilOffense
from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge
from expungeservice.models.charge_types.sex_crimes import SexCrime, RomeoAndJulietIneligibleSexCrime
from expungeservice.models.disposition import DispositionStatus, Disposition


@dataclass
class ChargeClassifier:
    violation_type: str
    name: str
    statute: str
    level: str
    chapter: str
    section: str
    disposition: Optional[Disposition]

    def classify(self) -> List[Type[Charge]]:
        def classification_found(c):
            return c is not None

        for c in self.__classifications_list():
            if classification_found(c):
                return c

        return [UnclassifiedCharge]

    def __classifications_list(self) -> Iterator[List[Type[Charge]]]:
        yield ChargeClassifier._juvenile_charge(self.violation_type)
        yield ChargeClassifier._contempt_of_court(self.name)
        yield ChargeClassifier._civil_offense(self.statute, self.chapter, self.name.lower())
        yield ChargeClassifier._traffic_crime(self.statute, self.level, self.disposition)
        yield ChargeClassifier._parking_ticket(self.violation_type)
        yield ChargeClassifier._violation(self.level)
        yield ChargeClassifier._dismissed_charge(self.disposition)
        yield from ChargeClassifier._drug_crime(self.statute, self.section, self.name.lower(), self.level)
        yield ChargeClassifier._subsection_6(self.section, self.level, self.statute)
        yield ChargeClassifier._classification_by_level(self.level, self.statute)

    @staticmethod
    def _dismissed_charge(disposition: Optional[Disposition]):
        if ChargeClassifier._is_dimissed(disposition):
            return [DismissedCharge]

    @staticmethod
    def _juvenile_charge(violation_type: str):
        if "juvenile" in violation_type.lower():
            return [JuvenileCharge]

    @staticmethod
    def _violation(level):
        if "Violation" in level:
            return [Violation]

    @staticmethod
    def _drug_crime(statute, section, name, level):
        yield ChargeClassifier._marijuana_ineligible(statute, section)
        yield ChargeClassifier._marijuana_eligible(section, name)
        yield ChargeClassifier._manufacture_delivery(name, level, statute)
        yield ChargeClassifier._sex_crime(level, statute)

    @staticmethod
    def _classification_by_level(level, statute):
        if "Misdemeanor" in level:
            return [Misdemeanor]
        if level == "Felony Class C":
            return [FelonyClassC]
        if level == "Felony Class B":
            if ChargeClassifier._person_felony(statute):
                return [PersonFelonyClassB]
            else:
                return [FelonyClassB]
        if level == "Felony Class A":
            return [FelonyClassA]

    @staticmethod
    def _marijuana_ineligible(statute, section):
        ineligible_statutes = ["475B359", "475B367", "475B371", "167262"]
        if statute == "475B3493C" or section in ineligible_statutes:
            return [MarijuanaIneligible]

    @staticmethod
    def _marijuana_eligible(section, name):
        if section == "475860" or "marij" in name or "mj" in name.split():
            return [MarijuanaEligible]

    @staticmethod
    def _manufacture_delivery(name, level, statute):
        if any([keyword in name for keyword in ["delivery", "manu/del", "manufactur"]]):
            if "2" in name:
                if level == "Felony Unclassified":
                    return [FelonyClassA, FelonyClassB]
                else:
                    return ChargeClassifier._classification_by_level(level, statute)
            elif "3" in name or "4" in name:
                if level == "Felony Unclassified":
                    return [FelonyClassA, FelonyClassB, FelonyClassC]
                else:
                    return ChargeClassifier._classification_by_level(level, statute)
            else:
                # The name contains either a "1" or no schedule number, and is possibly a marijuana charge.
                if level == "Felony Unclassified":
                    return [FelonyClassA, FelonyClassB, FelonyClassC, MarijuanaEligible]
                else:
                    return [MarijuanaEligible] + ChargeClassifier._classification_by_level(level, statute)

    @staticmethod
    def _subsection_6(section, level, statute):
        conditionally_ineligible_statutes = [
            "163200",  #  (Criminal mistreatment in the second degree) if the victim at the time of the crime was 65 years of age or older.
            "163205",  # (Criminal mistreatment in the first degree) if the victim at the time of the crime was 65 years of age or older, or when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions).
            "163575",  #  (Endangering the welfare of a minor) (1)(a), when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions).
            "163145",  # (Criminally negligent homicide), when that offense was punishable as a Class C felony.
            "163165",  # ( ineligible if under subection(1)(h) ; Assault in the third degree of a minor 10 years or younger)
        ]
        if section in conditionally_ineligible_statutes:
            return [Subsection6] + ChargeClassifier._classification_by_level(level, statute)

    @staticmethod
    def _traffic_crime(statute, level, disposition):
        chapter = statute[:3]
        if chapter.isdigit():
            statute_range = range(801, 826)
            chapter_num = int(chapter)
            if chapter_num == 813:
                if ChargeClassifier._is_dimissed(disposition):
                    return [DismissedCharge, DivertedDuii]
                else:
                    return [Duii]
            if chapter_num in statute_range:
                level_str = level.lower()
                if "felony" in level_str or "misdemeanor" in level_str:
                    if ChargeClassifier._is_dimissed(disposition):
                        return [DismissedCharge]
                    else:
                        return [TrafficNonViolation]
                else:
                    return [TrafficViolation]

    @staticmethod
    def _contempt_of_court(name):
        if "contempt of court" in name.lower():
            return [ContemptOfCourt]

    @staticmethod
    def _civil_offense(statute, chapter, name):
        statute_range = range(1, 100)
        if chapter:
            if chapter.isdigit() and int(chapter) in statute_range:
                return [CivilOffense]
        elif statute.isdigit() and int(statute) in statute_range:
            return [CivilOffense]
        elif "fugitive complaint" in name:
            return [CivilOffense]

    @staticmethod
    def _parking_ticket(violation_type):
        if "parking" in violation_type.lower():
            return [ParkingTicket]

    @staticmethod
    def _person_felony(statute):
        """
        The statutes listed here are specified in https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=712
        The list includes statutes which are not named as class B felonies. However, because a statute can be charged as a different level of crime from that named in the statute, our expunger checks OECI directly for whether the charge was a class B felony, and then checks membership in this list.
        """
        return statute in PersonFelonyClassB.statutes or statute in [
            full_statute[:6] for full_statute in PersonFelonyClassB.statutes_with_subsection
        ]

    @staticmethod
    def _sex_crime(level, statute):
        if statute in SexCrime.statutes:
            return [SexCrime]
        elif statute in SexCrime.romeo_and_juliet_exceptions:
            return [RomeoAndJulietIneligibleSexCrime] + ChargeClassifier._classification_by_level(level, statute)

    # TODO: Deduplicate with charge.dismissed()
    @staticmethod
    def _is_dimissed(disposition: Optional[Disposition]):
        return disposition and disposition.status in [
            DispositionStatus.NO_COMPLAINT,
            DispositionStatus.DISMISSED,
            DispositionStatus.DIVERTED,
        ]
