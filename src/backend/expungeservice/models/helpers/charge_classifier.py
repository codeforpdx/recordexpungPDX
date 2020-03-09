from dataclasses import dataclass

from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge
from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.traffic_non_violation import TrafficNonViolation
from expungeservice.models.charge_types.duii import Duii
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
from expungeservice.models.charge_types.sex_crimes import SexCrime
from expungeservice.models.charge_types.manufacture_delivery import ManufactureDelivery


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
        yield from ChargeClassifier._drug_crime(self.statute,  self.section, self.name.lower())
        yield from ChargeClassifier._classification_by_statute(self.statute, self.chapter, self.section, self.level)
        yield ChargeClassifier._parking_ticket(self.violation_type)
        yield from ChargeClassifier._classification_by_level(self.level, self.statute)
        yield ChargeClassifier._contempt_of_court(self.name)
        yield ChargeClassifier._civil_offense(self.statute, self.chapter, self.name.lower())

        yield UnclassifiedCharge

    @staticmethod
    def _juvenile_charge(violation_type):
        if "juvenile" in violation_type.lower():
            return JuvenileCharge

    @staticmethod
    def _drug_crime(statute, section, name):
        yield ChargeClassifier._marijuana_ineligible(statute, section)
        yield ChargeClassifier._marijuana_eligible(section, name)
        yield ChargeClassifier._manufacture_delivery(name)
        yield ChargeClassifier._sex_crime(statute)

    @staticmethod
    def _classification_by_statute(statute, chapter, section, level):
        yield ChargeClassifier._subsection_6(section, level)

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
    def _marijuana_eligible(section, name):
        if (section == "475860" or
            "marij" in name or
            "mj" in name.split()
            ):
            return MarijuanaEligible


    @staticmethod
    def _manufacture_delivery(name):
        if any([keyword in name for keyword in ["delivery", "manu/del", "manufactur"]]):
            if "2" in name:
                return None # This is schedule 2 and will get picked up by normal "Felony" eligibility rules.
            else:
                return ManufactureDelivery # The name contains either a "1" or no schedule number, and is possibly a marijuana charge.

    @staticmethod
    def _subsection_6(section, level):
        conditionally_ineligible_statutes = [
            "163200",  #  (Criminal mistreatment in the second degree) if the victim at the time of the crime was 65 years of age or older.
            "163205",  # (Criminal mistreatment in the first degree) if the victim at the time of the crime was 65 years of age or older, or when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions).
            "163575",  #  (Endangering the welfare of a minor) (1)(a), when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions).
            "163145",  # (Criminally negligent homicide), when that offense was punishable as a Class C felony.
            "163165",  # ( ineligible if under subection(1)(h) ; Assault in the third degree of a minor 10 years or younger)
        ]
        if section in conditionally_ineligible_statutes:
            return Subsection6

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
    def _contempt_of_court(name):
        if "contempt of court" in name.lower():
            return ContemptOfCourt
                            
    @staticmethod
    def _civil_offense(statute, chapter, name):
        statute_range = range(1, 100)
        if chapter:
            if chapter.isdigit() and int(chapter) in statute_range:
                return CivilOffense
        elif statute.isdigit() and int(statute) in statute_range:
            return CivilOffense
        elif "fugitive complaint" in name:
            return CivilOffense

    @staticmethod
    def _parking_ticket(violation_type):
        if "parking" in violation_type.lower():
            return ParkingTicket

    @staticmethod
    def _non_traffic_violation(level):
        if "Violation" in level:
            return Violation

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

    @staticmethod
    def _sex_crime(statute):
        if statute in SexCrime.statutes + SexCrime.romeo_and_juliet_exceptions:
            return SexCrime
