from dataclasses import dataclass
from math import ceil
from typing import List, Iterator, Type, Optional

from expungeservice.models.ambiguous import AmbiguousChargeTypeWithQuestion
from expungeservice.models.charge import Charge
from expungeservice.models.charge_types.dismissed_charge import DismissedCharge
from expungeservice.models.charge_types.juvenile_charge import JuvenileCharge
from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from expungeservice.models.charge_types.severe_charge import SevereCharge
from expungeservice.models.charge_types.traffic_violation import TrafficViolation
from expungeservice.models.charge_types.traffic_offense import TrafficOffense
from expungeservice.models.charge_types.duii import Duii, DivertedDuii
from expungeservice.models.charge_types.subsection_6 import Subsection6
from expungeservice.models.charge_types.marijuana_ineligible import MarijuanaIneligible
from expungeservice.models.charge_types.marijuana_eligible import (
    MarijuanaEligible,
    MarijuanaUnder21,
    MarijuanaViolation,
)
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.charge_types.violation import Violation
from expungeservice.models.charge_types.reduced_to_violation import ReducedToViolation
from expungeservice.models.charge_types.parking_ticket import ParkingTicket
from expungeservice.models.charge_types.fare_violation import FareViolation
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.models.charge_types.civil_offense import CivilOffense
from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge
from expungeservice.models.charge_types.sex_crimes import (
    SexCrime,
    RomeoAndJulietIneligibleSexCrime,
    RomeoAndJulietNMASexCrime,
)
from expungeservice.models.disposition import DispositionStatus, Disposition


@dataclass
class ChargeClassifier:
    violation_type: str
    name: str
    statute: str
    level: str
    section: str
    birth_year: Optional[int]
    disposition: Disposition

    def classify(self) -> AmbiguousChargeTypeWithQuestion:
        def classification_found(c):
            return c is not None

        for c in self.__classifications_list():
            if classification_found(c):
                return c

        return AmbiguousChargeTypeWithQuestion([UnclassifiedCharge])

    def __classifications_list(self) -> Iterator[AmbiguousChargeTypeWithQuestion]:
        name = self.name.lower()
        yield ChargeClassifier._juvenile_charge(self.violation_type)
        yield ChargeClassifier._parking_ticket(self.violation_type)
        yield ChargeClassifier._fare_violation(name)
        yield ChargeClassifier._civil_offense(self.statute, name)
        yield ChargeClassifier._traffic_crime(self.statute, name, self.level, self.disposition)
        yield ChargeClassifier._marijuana_violation(name, self.level)
        yield ChargeClassifier._violation(self.level, name)
        criminal_charge = next(
            (
                c
                for c in ChargeClassifier._criminal_charge(
                    self.statute, self.section, self.name, self.level, self.birth_year, self.disposition
                )
                if c
            ),
            None,
        )
        if criminal_charge and ChargeClassifier._is_dimissed(self.disposition):
            yield AmbiguousChargeTypeWithQuestion([DismissedCharge])
        elif criminal_charge:
            yield criminal_charge

    @staticmethod
    def _criminal_charge(
        statute, section, name, level, birth_year, disposition
    ) -> Iterator[AmbiguousChargeTypeWithQuestion]:
        yield from ChargeClassifier._drug_crime(statute, section, name.lower(), level, birth_year, disposition)
        yield ChargeClassifier._subsection_6(section, level, statute)
        yield ChargeClassifier._severe_unclassified_charges(name.lower(), statute)
        yield ChargeClassifier._other_criminal_charges(statute)
        yield ChargeClassifier._classification_by_level(level, statute)

    @staticmethod
    def _juvenile_charge(violation_type: str):
        if "juvenile" in violation_type.lower():
            return AmbiguousChargeTypeWithQuestion([JuvenileCharge])

    @staticmethod
    def _violation(level, name):
        if "Violation" in level:
            if "reduced" in name or "treated as" in name:
                return AmbiguousChargeTypeWithQuestion([ReducedToViolation])
            else:
                return AmbiguousChargeTypeWithQuestion([Violation])

    @staticmethod
    def _drug_crime(
        statute, section, name, level, birth_year, disposition
    ) -> Iterator[AmbiguousChargeTypeWithQuestion]:
        yield ChargeClassifier._marijuana_ineligible(statute, section)
        yield ChargeClassifier._marijuana_eligible(section, name, birth_year, disposition)
        yield ChargeClassifier._manufacture_delivery(name, level, statute)
        yield ChargeClassifier._sex_crime(statute)

    @staticmethod
    def _severe_unclassified_charges(name, statute):
        treason_statute = "166005"
        if "murder" in name or statute == treason_statute:
            return AmbiguousChargeTypeWithQuestion([SevereCharge])

    @staticmethod
    def _other_criminal_charges(statute):
        possession_of_weapon_by_prison_inmate = "166275"
        if statute == possession_of_weapon_by_prison_inmate:
            return AmbiguousChargeTypeWithQuestion([FelonyClassA])

    @staticmethod
    def _classification_by_level(level, statute):
        if "Misdemeanor" in level:
            return AmbiguousChargeTypeWithQuestion([Misdemeanor])
        if level == "Felony Class C":
            return AmbiguousChargeTypeWithQuestion([FelonyClassC])
        if level == "Felony Class B":
            if ChargeClassifier._person_felony(statute):
                return AmbiguousChargeTypeWithQuestion([PersonFelonyClassB])
            else:
                return AmbiguousChargeTypeWithQuestion([FelonyClassB])
        if level == "Felony Class A":
            return AmbiguousChargeTypeWithQuestion([FelonyClassA])
        if level == "Felony Unclassified":
            question_string = "Was the charge for an A Felony, B Felony, or C Felony?"
            options = ["A Felony", "B Felony", "C Felony"]
            return AmbiguousChargeTypeWithQuestion([FelonyClassA, FelonyClassB, FelonyClassC], question_string, options)

    @staticmethod
    def _marijuana_ineligible(statute, section):
        ineligible_statutes = ["475B359", "475B367", "475B371", "167262"]
        if statute == "475B3493C" or section in ineligible_statutes:
            return AmbiguousChargeTypeWithQuestion([MarijuanaIneligible])

    @staticmethod
    def _marijuana_violation(name, level):
        if ("marij" in name or "mj" in name.split()) and "Violation" in level:
            return AmbiguousChargeTypeWithQuestion([MarijuanaViolation])

    @staticmethod
    def _marijuana_eligible(section, name, birth_year, disposition):
        if section == "475860" or "marij" in name or "mj" in name.split():
            if birth_year and disposition.status != DispositionStatus.UNKNOWN:
                convicted_age = ceil(disposition.date.year - birth_year)
                if convicted_age < 21:
                    return AmbiguousChargeTypeWithQuestion([MarijuanaUnder21])
            return AmbiguousChargeTypeWithQuestion([MarijuanaEligible])

    @staticmethod
    def _manufacture_delivery(name, level, statute):
        if any([manu_del_keyword in name for manu_del_keyword in ["delivery", "manu/del", "manufactur"]]):
            if any([schedule_2_keyword in name for schedule_2_keyword in ["2", "ii", "heroin", "cocaine", "meth"]]):
                if level == "Felony Unclassified":
                    question_string = "Was the charge for an A Felony or B Felony?"
                    options = ["A Felony", "B Felony"]
                    return AmbiguousChargeTypeWithQuestion([FelonyClassA, FelonyClassB], question_string, options)
            elif any([schedule_3_keyword in name for schedule_3_keyword in ["3", "iii", "4", " iv"]]):
                return ChargeClassifier._classification_by_level(level, statute)
            else:
                # The name contains either a "1" or no schedule number, and is possibly a marijuana charge.
                if level == "Felony Unclassified":
                    question_string = "Was the underlying substance marijuana, and if not, was the charge for an A Felony, B Felony, or C Felony?"
                    options = ["Yes", "No: A Felony", "No: B Felony", "No: C Felony"]
                    return AmbiguousChargeTypeWithQuestion(
                        [MarijuanaEligible, FelonyClassA, FelonyClassB, FelonyClassC], question_string, options
                    )
                elif level == "Felony Class A" or level == "Felony Class B":
                    question_string = "Was the underlying substance marijuana?"
                    options = ["Yes", "No"]
                    charge_type_by_level = ChargeClassifier._classification_by_level(
                        level, statute
                    ).ambiguous_charge_type
                    return AmbiguousChargeTypeWithQuestion(
                        [MarijuanaEligible] + charge_type_by_level, question_string, options
                    )

    @staticmethod
    def _subsection_6(section, level, statute):
        mistreatment_one = "163205"  #  (Criminal mistreatment in the second degree) if the victim at the time of the crime was 65 years of age or older.
        mistreatment_two = "163200"  # (Criminal mistreatment in the first degree) if the victim at the time of the crime was 65 years of age or older, or when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions).
        endangering_welfare = "163575"  #  (Endangering the welfare of a minor) (1)(a), when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions).
        negligent_homicide = (
            "163145"  # (Criminally negligent homicide), when that offense was punishable as a Class C felony.
        )
        assault_three = "163165"  # ( ineligible if under subection(1)(h) ; Assault in the third degree of a minor 10 years or younger)
        if section == mistreatment_one:
            question_string = "Was the victim between the ages of 18 and 65?"
            options = ["Yes", "No"]
            charge_type_by_level = ChargeClassifier._classification_by_level(level, statute).ambiguous_charge_type
            return AmbiguousChargeTypeWithQuestion(charge_type_by_level + [Subsection6], question_string, options)
        elif section == mistreatment_two:
            question_string = "Was the victim older than 65?"
            options = ["Yes", "No"]
            charge_type_by_level = ChargeClassifier._classification_by_level(level, statute).ambiguous_charge_type
            return AmbiguousChargeTypeWithQuestion([Subsection6] + charge_type_by_level, question_string, options)
        elif section == endangering_welfare:
            question_string = "Was the charge for physical abuse?"
            options = ["Yes", "No"]
            charge_type_by_level = ChargeClassifier._classification_by_level(level, statute).ambiguous_charge_type
            return AmbiguousChargeTypeWithQuestion([Subsection6] + charge_type_by_level, question_string, options)
        elif section == assault_three:
            question_string = "Was the victim more than ten years old?"
            options = ["Yes", "No"]
            charge_type_by_level = ChargeClassifier._classification_by_level(level, statute).ambiguous_charge_type
            return AmbiguousChargeTypeWithQuestion(charge_type_by_level + [Subsection6], question_string, options)
        elif section == negligent_homicide and level == "Felony Class C":
            return AmbiguousChargeTypeWithQuestion([Subsection6])

    @staticmethod
    def _traffic_crime(statute, name, level, disposition):
        chapter = statute[:3]
        if chapter.isdigit():
            statute_range = [481, 482, 483] + list(range(801, 826))
            chapter_num = int(chapter)
            if chapter_num == 813:
                if ChargeClassifier._is_dimissed(disposition):
                    question_string = "Was the charge dismissed pursuant to a court-ordered diversion program?"
                    options = ["Yes", "No"]
                    return AmbiguousChargeTypeWithQuestion([DivertedDuii, DismissedCharge], question_string, options)
                else:
                    return AmbiguousChargeTypeWithQuestion([Duii])
            if chapter_num in statute_range:
                level_str = level.lower()
                if "felony" in level_str or "misdemeanor" in level_str:
                    if ChargeClassifier._is_dimissed(disposition):
                        return AmbiguousChargeTypeWithQuestion([DismissedCharge])
                    else:
                        return AmbiguousChargeTypeWithQuestion([TrafficOffense])
                else:
                    return AmbiguousChargeTypeWithQuestion([TrafficViolation])
        if name == "pedestrian j-walking":
            return AmbiguousChargeTypeWithQuestion([TrafficViolation])

    @staticmethod
    def _civil_offense(statute, name):
        statute_range = range(1, 100)
        chapter = ChargeClassifier._build_chapter_for_civil_offense(statute)
        if chapter:
            if chapter.isdigit() and int(chapter) in statute_range:
                return AmbiguousChargeTypeWithQuestion([CivilOffense])
        elif statute.isdigit() and int(statute) in statute_range:
            return AmbiguousChargeTypeWithQuestion([CivilOffense])
        elif "fugitive" in name:
            return AmbiguousChargeTypeWithQuestion([CivilOffense])
        elif "contempt of court" in name:
            return AmbiguousChargeTypeWithQuestion([CivilOffense])

    @staticmethod
    def _build_chapter_for_civil_offense(statute):
        if "." in statute:
            return statute.split(".")[0]
        elif len(statute) == 4:
            # When the statue has no period
            return statute[:2]
        else:
            return None

    @staticmethod
    def _parking_ticket(violation_type):
        if "parking" in violation_type.lower():
            return AmbiguousChargeTypeWithQuestion([ParkingTicket])

    @staticmethod
    def _fare_violation(name):
        if "fare violation" in name or "non-payment of fare" in name:
            return AmbiguousChargeTypeWithQuestion([FareViolation])

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
    def _sex_crime(statute):
        if statute in SexCrime.statutes:
            return AmbiguousChargeTypeWithQuestion([SexCrime])
        elif statute in SexCrime.romeo_and_juliet_exceptions:
            question_string = """
            Select "Yes" if ALL of the following are true:
            1. The victim's lack of consent was solely due to age (statutory rape) AND
            2. You were under 23 years old when the act occurred AND
            3. The victim was less than five years younger than you when the act occurred
            """
            options = ["Yes (Rare, contact michael@qiu-qiulaw.com)", "No"]
            return AmbiguousChargeTypeWithQuestion(
                [RomeoAndJulietNMASexCrime, RomeoAndJulietIneligibleSexCrime], question_string, options
            )

    # TODO: Deduplicate with charge.dismissed()
    @staticmethod
    def _is_dimissed(disposition: Disposition):
        return disposition.status in [
            DispositionStatus.NO_COMPLAINT,
            DispositionStatus.DISMISSED,
            DispositionStatus.DIVERTED,
        ]
