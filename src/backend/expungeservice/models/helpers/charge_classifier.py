from dataclasses import dataclass

from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge
from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.traffic_non_violation import TrafficNonViolation
from expungeservice.models.charge_types.duii import Duii
from expungeservice.models.charge_types.subsection_12 import Subsection12
from expungeservice.models.charge_types.subsection_6 import Subsection6
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.charge_types.non_traffic_violation import NonTrafficViolation
from expungeservice.models.charge_types.parking_ticket import ParkingTicket
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
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
        yield from ChargeClassifier._classification_by_statute(self.statute, self.chapter, self.section, self.level)
        yield ChargeClassifier._parking_ticket(self.violation_type)
        yield from ChargeClassifier._classification_by_level(self.level, self.statute)
        yield ChargeClassifier._civil_offense(self.statute, self.chapter, self.name)

        yield UnclassifiedCharge

    @staticmethod
    def _juvenile_charge(violation_type):
        if "juvenile" in violation_type.lower():
            return JuvenileCharge

    @staticmethod
    def _classification_by_statute(statute, chapter, section, level):
        yield ChargeClassifier._marijuana_ineligible(statute, section)
        yield ChargeClassifier._subsection_12(section)
        yield ChargeClassifier._subsection_6(section, level)
        yield ChargeClassifier._schedule_1_pcs(section)

    @staticmethod
    def _classification_by_level(level, statute):
        yield ChargeClassifier._non_traffic_violation(level)
        yield ChargeClassifier._misdemeanor(level)
        yield ChargeClassifier._felony_class_c(level)
        yield ChargeClassifier._felony_class_b(level, statute)
        yield ChargeClassifier._felony_class_a(level)

    @staticmethod
    def _marijuana_ineligible(statute, section):
        ineligible_statutes = ["475B359", "475B367", "475B371", "167262"]
        if statute == "475B3493C" or section in ineligible_statutes:
            return MarijuanaIneligible

    @staticmethod
    def _subsection_6(section, level):
        conditionally_ineligible_statutes = [
            "163200",  #  (Criminal mistreatment in the second degree) if the victim at the time of the crime was 65 years of age or older.
            "163205",  # (overrides subsection 12.(Criminal mistreatment in the first degree) if the victim at the time of the crime was 65 years of age or older, or when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions).
            "163575",  #  (Endangering the welfare of a minor) (1)(a), when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions).
            "163145",  # (Criminally negligent homicide), when that offense was punishable as a Class C felony.
            "163165",  # ( ineligible if under subection(1)(h) ; Assault in the third degree of a minor 10 years or younger)
        ]
        if section in conditionally_ineligible_statutes and level not in ["Felony Class A", "Felony Class B"]:
            return Subsection6

    @staticmethod
    def _subsection_12(section):
        if section in (Subsection12.conditionally_eligible_sections + Subsection12.eligible_sections):
            return Subsection12

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
    def _felony_class_b(level, statute):
        if level == "Felony Class B":
            if ChargeClassifier._person_felony(statute):
                return PersonFelonyClassB
            else:
                return FelonyClassB

    @staticmethod
    def _felony_class_a(level):
        if level == "Felony Class A":
            return FelonyClassA

    @staticmethod
    def _person_felony(statute):
        """
        The statutes listed here are specified in https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=712
        The list includes statutes which are not named as class B felonies. However, because a statute can be charged as a different level of crime from that named in the statute, our expunger checks OECI directly for whether the charge was a class B felony, and then checks membership in this list.
        """
        if statute in PersonFelonyClassB.statutes + PersonFelonyClassB.statutes_with_subsection:
            return True
        elif statute in [full_statute[:6] for full_statute in PersonFelonyClassB.statutes_with_subsection]:
            return True
            # In this case the type eligibility needs more analysis. The condition is checked again in the charge object's type eligibility method.
        else:
            return False
