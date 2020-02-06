from dataclasses import dataclass

from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge
from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.traffic_non_violation import TrafficNonViolation
from expungeservice.models.charge_types.duii import Duii
from expungeservice.models.charge_types.subsection_12 import Subsection12
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.charge_types.non_traffic_violation import NonTrafficViolation
from expungeservice.models.charge_types.parking_ticket import ParkingTicket
from expungeservice.models.charge_types.person_crime import PersonCrime
from expungeservice.models.charge_types.schedule_1_p_c_s import Schedule1PCS
from expungeservice.models.charge_types.civil_offense import CivilOffense
from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge


@dataclass
class ChargeClassifier:
    violation_type: str
    name: str
    statute: str
    level: str
    chapter: str
    section: str

    def classify(self):
        def classification_found(c):
            return c is not None

        for c in self.__classifications_list():
            if classification_found(c):
                return c

    def __classifications_list(self):
        yield ChargeClassifier._juvenile_charge(self.violation_type)
        yield ChargeClassifier._traffic_crime(self.statute, self.level)
        yield from ChargeClassifier._classification_by_statute(self.statute, self.chapter, self.section)
        yield ChargeClassifier._parking_ticket(self.violation_type)
        yield from ChargeClassifier._classification_by_level(self.level)
        yield ChargeClassifier._civil_offense(self.statute, self.chapter, self.name)

        yield UnclassifiedCharge

    @staticmethod
    def _juvenile_charge(violation_type):
        if "juvenile" in violation_type.lower():
            return JuvenileCharge

    @staticmethod
    def _classification_by_statute(statute, chapter, section):
        yield ChargeClassifier._marijuana_ineligible(statute, section)
        yield ChargeClassifier._subsection_12(section)
        yield ChargeClassifier._crime_against_person(section)
        yield ChargeClassifier._schedule_1_pcs(section)

    @staticmethod
    def _classification_by_level(level):
        yield ChargeClassifier._non_traffic_violation(level)
        yield ChargeClassifier._misdemeanor(level)
        yield ChargeClassifier._felony_class_c(level)
        yield ChargeClassifier._felony_class_b(level)
        yield ChargeClassifier._felony_class_a(level)

    @staticmethod
    def _marijuana_ineligible(statute, section):
        ineligible_statutes = ["475B359", "475B367", "475B371", "167262"]
        if statute == "475B3493C" or section in ineligible_statutes:
            return MarijuanaIneligible

    @staticmethod
    def _subsection_12(section):
        ineligible_statutes = [
            "163200",
            "163205",
            "163575",
            "163535",
            "163175",
            "163275",
            "162165",
            "163525",
            "164405",
            "164395",
            "162185",
            "166220",
            "163225",
            "163165",
        ]
        if section in ineligible_statutes:
            return Subsection12

    @staticmethod
    def _crime_against_person(section):
        statute_ranges = (range(163305, 163480), range(163670, 163694), range(167008, 167108), range(167057, 167081))
        if section.isdigit() and any(int(section) in statute_range for statute_range in statute_ranges):
            return PersonCrime

    @staticmethod
    def _traffic_crime(statute, level):

        chapter = statute[:3]
        if chapter.isdigit():
            statute_range = range(801, 826)

            chapter_num = int(chapter)

            if chapter_num == 813:
                return Duii

            elif chapter_num in statute_range:
                level_str = level.lower()
                if "felony" in level_str or "misdemeanor" in level_str:
                    return TrafficNonViolation
                else:
                    return TrafficViolation

    @staticmethod
    def _civil_offense(statute, chapter, name):
        statute_range = range(1, 100)
        if chapter:
            if chapter.isdigit() and int(chapter) in statute_range:
                return CivilOffense
        elif statute.isdigit() and int(statute) in statute_range:
            return CivilOffense
        elif "fugitive complaint" in name.lower():
            return CivilOffense

    @staticmethod
    def _schedule_1_pcs(section):
        if section in ["475854", "475874", "475884", "475894", "475992"]:
            return Schedule1PCS

    @staticmethod
    def _parking_ticket(violation_type):
        if "parking" in violation_type.lower():
            return ParkingTicket

    @staticmethod
    def _non_traffic_violation(level):
        if "Violation" in level:
            return NonTrafficViolation

    @staticmethod
    def _misdemeanor(level):
        if "Misdemeanor" in level:
            return Misdemeanor

    @staticmethod
    def _felony_class_c(level):
        if level == "Felony Class C":
            return FelonyClassC

    @staticmethod
    def _felony_class_b(level):
        if level == "Felony Class B":
            return FelonyClassB

    @staticmethod
    def _felony_class_a(level):
        if level == "Felony Class A":
            return FelonyClassA
