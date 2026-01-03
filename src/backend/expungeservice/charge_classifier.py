from dataclasses import dataclass, replace
from math import ceil
from typing import Iterator, Optional, Dict

from expungeservice.models.ambiguous import AmbiguousChargeTypeWithQuestion
from expungeservice.models.charge import ChargeType
from expungeservice.models.charge_types.criminal_forfeiture import CriminalForfeiture
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
    MarijuanaManufactureDelivery,
)
from expungeservice.models.charge_types.misdemeanor_class_a import MisdemeanorClassA
from expungeservice.models.charge_types.misdemeanor_class_bc import MisdemeanorClassBC
from expungeservice.models.charge_types.violation import Violation
from expungeservice.models.charge_types.reduced_to_violation import ReducedToViolation
from expungeservice.models.charge_types.possible_traffic_violation import PossibleTrafficViolation
from expungeservice.models.charge_types.parking_ticket import ParkingTicket
from expungeservice.models.charge_types.fare_violation import FareViolation
from expungeservice.models.charge_types.person_felony import PersonFelonyClassB
from expungeservice.models.charge_types.civil_offense import CivilOffense
from expungeservice.models.charge_types.contempt_of_court import ContemptOfCourt, SevereContemptOfCourt
from expungeservice.models.charge_types.unclassified_charge import UnclassifiedCharge
from expungeservice.models.charge_types.sex_crimes import (
    SexCrime,
    RomeoAndJulietIneligibleSexCrime,
    RomeoAndJulietNMASexCrime,
)
from expungeservice.models.disposition import DispositionStatus, Disposition
from expungeservice.models.record import Question, Answer
from expungeservice.models.charge_types.lesser_charge import LesserChargeEligible, LesserChargeIneligible


@dataclass
class ChargeClassifier:
    violation_type: str
    name: str
    statute: str
    level: str
    section: str
    birth_year: Optional[int]
    disposition: Disposition
    location: str

    def classify(self) -> AmbiguousChargeTypeWithQuestion:
        def classification_found(c):
            return c is not None

        for c in self.__classifications_list():
            if classification_found(c):
                return c

        return AmbiguousChargeTypeWithQuestion([UnclassifiedCharge()])

    def __classifications_list(self) -> Iterator[AmbiguousChargeTypeWithQuestion]:
        name = self.name.lower()
        level = self.level.lower()
        location = self.location.lower()
        yield ChargeClassifier._lesser_charge(self.disposition)
        yield ChargeClassifier._juvenile_charge(self.violation_type)
        yield ChargeClassifier._parking_ticket(self.violation_type)
        yield ChargeClassifier._fare_violation(name)
        yield ChargeClassifier._contempt_of_court(name)
        yield ChargeClassifier._civil_offense(self.statute, name)
        yield ChargeClassifier._criminal_forfeiture(self.statute)
        yield ChargeClassifier._traffic_crime(self.statute, name, level, self.disposition)
        yield ChargeClassifier._marijuana_violation(name, level)
        yield ChargeClassifier._violation(level, name, location)
        criminal_charge = next(
            (
                c
                for c in ChargeClassifier._criminal_charge(
                    self.statute, self.section, name, level, self.birth_year, self.disposition
                )
                if c
            ),
            None,
        )
        if criminal_charge and ChargeClassifier._is_dimissed(self.disposition):
            yield AmbiguousChargeTypeWithQuestion([DismissedCharge()])
        elif criminal_charge:
            yield criminal_charge

    @staticmethod
    def _criminal_charge(
        statute, section, name, level, birth_year, disposition
    ) -> Iterator[AmbiguousChargeTypeWithQuestion]:
        yield from ChargeClassifier._drug_crime(statute, section, name, level, birth_year, disposition)
        yield ChargeClassifier._subsection_6(section, level, statute)
        yield ChargeClassifier._severe_unclassified_charges(name, statute)
        yield ChargeClassifier._other_criminal_charges(statute)
        yield ChargeClassifier._attempt_to_commit(name, level, statute)
        yield ChargeClassifier._classification_by_level(level, statute)

    @staticmethod
    def _lesser_charge(dispostion: Disposition):
        if dispostion.lesser_charge:
            question_string = "Is the convicted charge on this case that this charge was reduced to eligible?"
            options = {"Yes": LesserChargeEligible(), "No": LesserChargeIneligible()}
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)

    @staticmethod
    def _juvenile_charge(violation_type: str):
        if "juvenile" in violation_type.lower():
            return AmbiguousChargeTypeWithQuestion([JuvenileCharge()])

    @staticmethod
    def _violation(level, name, location):
        if "violation" in level:
            if location == "multnomah":
                return AmbiguousChargeTypeWithQuestion([PossibleTrafficViolation()])
            else:
                if "reduced" in name or "treated as" in name:
                    return AmbiguousChargeTypeWithQuestion([ReducedToViolation()])
                else:
                    return AmbiguousChargeTypeWithQuestion([Violation()])

    @staticmethod
    def _drug_crime(
        statute, section, name, level, birth_year, disposition
    ) -> Iterator[AmbiguousChargeTypeWithQuestion]:
        yield ChargeClassifier._marijuana_ineligible(statute, section)
        yield ChargeClassifier._marijuana_eligible(section, name, birth_year, disposition, level)
        yield ChargeClassifier._pcs_and_manufacture_delivery(section, name, level, statute)
        yield ChargeClassifier._sex_crime(statute)

    @staticmethod
    def _severe_unclassified_charges(name, statute):
        treason_statute = "166005"
        if "murder" in name or statute == treason_statute:
            return AmbiguousChargeTypeWithQuestion([SevereCharge()])

    @staticmethod
    def _other_criminal_charges(statute):
        possession_of_weapon_by_prison_inmate = "166275"
        if statute == possession_of_weapon_by_prison_inmate:
            return AmbiguousChargeTypeWithQuestion([FelonyClassA()])

    @staticmethod
    def _attempt_to_commit(name, level, statute):
        if (level == "misdemeanor class a" or level == "felony class c") and "attempt to commit" in name:
            question_string = "Was the underlying conduct a sex crime or traffic offense?"
            charge_type_by_level = ChargeClassifier._classification_by_level(level, statute).ambiguous_charge_type[0]
            options = {"Yes; sex crime": SexCrime(), "Yes; traffic offense": TrafficOffense(), "No": charge_type_by_level}
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)
        if level == "felony class b" and "attempt to commit" in name:
            question_string = "Was this a drug-related or traffic-related charge?"
            drug_crime_question_string = "Was the underlying substance marijuana?"
            drug_crime_options = {
                "Yes": MarijuanaEligible(severity_level="Felony Class C"),
                "No": FelonyClassB(),
            }  # MJ Eligible reclassified as Felony Class C
            drug_crime_classification = ChargeClassifier._build_ambiguous_charge_type_with_question(
                drug_crime_question_string, drug_crime_options
            )
            drug_crime_question_id = f"{question_string}-Yes-{drug_crime_classification.question.question_id}"  # type: ignore
            drug_crime_question = replace(drug_crime_classification.question, question_id=drug_crime_question_id)
            charge_types = drug_crime_classification.ambiguous_charge_type + [PersonFelonyClassB(), TrafficOffense()]
            question = Question(
                question_string,
                question_string,
                {
                    "Yes; drug-related": Answer(question=drug_crime_question),
                    "Yes; traffic-related": Answer(edit={"charge_type": TrafficOffense.__name__}),
                    "No": Answer(edit={"charge_type": PersonFelonyClassB.__name__}),
                },
            )
            return AmbiguousChargeTypeWithQuestion(charge_types, question)
        if "attempt to commit" in name:  # for any other severity level
            question_string = "Was the underlying conduct a traffic crime?"
            charge_type_by_level = ChargeClassifier._classification_by_level(level, statute).ambiguous_charge_type[0]
            options = {"Yes": TrafficOffense(), "No": charge_type_by_level}
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)

    @staticmethod
    def _classification_by_level(level, statute):
        if "misdemeanor class b" in level or "misdemeanor class c" in level:
            return AmbiguousChargeTypeWithQuestion([MisdemeanorClassBC()])
        if "misdemeanor" in level:
            return AmbiguousChargeTypeWithQuestion([MisdemeanorClassA()])
        if level == "felony class c":
            return AmbiguousChargeTypeWithQuestion([FelonyClassC()])
        if level == "felony class b":
            if ChargeClassifier._person_felony(statute):
                return AmbiguousChargeTypeWithQuestion([PersonFelonyClassB()])
            else:
                return AmbiguousChargeTypeWithQuestion([FelonyClassB()])
        if level == "felony class a":
            return AmbiguousChargeTypeWithQuestion([FelonyClassA()])
        if level == "felony unclassified":
            question_string = "Was the charge for an A Felony, B Felony, or C Felony?"
            options = {"A Felony": FelonyClassA(), "B Felony": FelonyClassB(), "C Felony": FelonyClassC()}
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)

    @staticmethod
    def _marijuana_ineligible(statute, section):
        ineligible_statutes = ["475B359", "475B367", "475B371", "167262"]
        if statute == "475B3493C" or section in ineligible_statutes:
            return AmbiguousChargeTypeWithQuestion([MarijuanaIneligible()])

    @staticmethod
    def _marijuana_violation(name, level):
        if ("marij" in name or "mj" in name.split()) and "violation" in level:
            return AmbiguousChargeTypeWithQuestion([MarijuanaViolation()])

    @staticmethod
    def _marijuana_eligible(section, name, birth_year, disposition, level):
        if section == "475860" or "marij" in name or "mj" in name.split():
            if birth_year and disposition.status != DispositionStatus.UNKNOWN:
                convicted_age = ceil(disposition.date.year - birth_year)
                if convicted_age < 21:
                    return AmbiguousChargeTypeWithQuestion([MarijuanaUnder21()])
            if level == "felony class a" or level == "felony class b" or level == "felony unclassified":
                # MarijuanaEligible Felony Class C+ are reclassified as Felony Class C
                return AmbiguousChargeTypeWithQuestion([MarijuanaEligible(severity_level="Felony Class C")])
            else:
                # MarijuanaEligible Felony Class C and below are reclassified as Misdemeanor Class A
                return AmbiguousChargeTypeWithQuestion([MarijuanaEligible(severity_level="Misdemeanor Class A")])

    @staticmethod
    def _pcs_and_manufacture_delivery(section, name, level, statute):
        is_manudel = any([manu_del_keyword in name for manu_del_keyword in ["delivery", "manu/del", "manufactur"]])
        pcs_in_name = all(c in name for c in ["poss", "sub"]) or "pcs" in name
        is_pcs = section == "4759924A" or section == "4757521A" or pcs_in_name
        if is_manudel:
            return ChargeClassifier._handle_pcs_and_manufacture_delivery(
                name, level, statute, ChargeClassifier._manudel_schedule_2_handler
            )
        elif is_pcs:
            return ChargeClassifier._handle_pcs_and_manufacture_delivery(
                name, level, statute, ChargeClassifier._pcs_schedule_2_handler
            )

    @staticmethod
    def _manudel_schedule_2_handler(level):
        if level == "felony unclassified":
            question_string = "Was the charge for an A Felony or B Felony?"
            options = {"A Felony": FelonyClassA(), "B Felony": FelonyClassB()}
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)

    @staticmethod
    def _pcs_schedule_2_handler(level):
        if level == "felony unclassified":
            question_string = "Was the charge for a B Felony or C Felony?"
            options = {"B Felony": FelonyClassB(), "C Felony": FelonyClassC()}
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)

    @staticmethod
    def _handle_pcs_and_manufacture_delivery(name, level, statute, schedule_2_handler):
        if any([schedule_2_keyword in name for schedule_2_keyword in ["2", "ii", "heroin", "cocaine", "meth"]]):
            return schedule_2_handler(level)
        elif any([schedule_3_keyword in name for schedule_3_keyword in ["3", "iii", "4", " iv"]]):
            return ChargeClassifier._classification_by_level(level, statute)
        else:
            # The name contains either a "1" or no schedule number, and thus is possibly a marijuana charge.
            question_string = "Was the underlying substance marijuana?"
            charge_types_with_question = ChargeClassifier._classification_by_level(level, statute)
            if level == "felony unclassified":
                felony_unclassified_question_id = (
                    f"{question_string}-No-{charge_types_with_question.question.question_id}"
                )
                felony_unclassified_question = replace(
                    charge_types_with_question.question, question_id=felony_unclassified_question_id
                )
                charge_types = [MarijuanaManufactureDelivery()] + charge_types_with_question.ambiguous_charge_type
                question = Question(
                    question_string,
                    question_string,
                    {
                        "Yes": Answer(edit={"charge_type": MarijuanaManufactureDelivery.__name__}),
                        "No": Answer(question=felony_unclassified_question),
                    },
                )
                return AmbiguousChargeTypeWithQuestion(charge_types, question)
            elif level == "felony class a" or level == "felony class b":
                charge_type = charge_types_with_question.ambiguous_charge_type[0]
                options = {"Yes": MarijuanaManufactureDelivery(), "No": charge_type}
                return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)

    # TODO: Assert for when Felony Unclassified
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
            charge_type_by_level = ChargeClassifier._classification_by_level(level, statute).ambiguous_charge_type[0]
            question_string = "Was the victim between the ages of 18 and 65?"
            options = {"Yes": charge_type_by_level, "No": Subsection6()}
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)
        elif section == mistreatment_two:
            charge_type_by_level = ChargeClassifier._classification_by_level(level, statute).ambiguous_charge_type[0]
            question_string = "Was the victim older than 65?"
            options = {"Yes": Subsection6(), "No": charge_type_by_level}
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)
        elif section == endangering_welfare:
            charge_type_by_level = ChargeClassifier._classification_by_level(level, statute).ambiguous_charge_type[0]
            question_string = "Was the charge for physical abuse?"
            options = {"Yes": Subsection6(), "No": charge_type_by_level}
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)
        elif section == assault_three:
            charge_type_by_level = ChargeClassifier._classification_by_level(level, statute).ambiguous_charge_type[0]
            question_string = "Was the victim more than ten years old?"
            options = {"Yes": charge_type_by_level, "No": Subsection6()}
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)
        elif section == negligent_homicide and level == "felony class c":
            return AmbiguousChargeTypeWithQuestion([Subsection6()])

    @staticmethod
    def _traffic_crime(statute, name, level, disposition):
        chapter = statute[:3]
        if chapter.isdigit():
            statute_range = [481, 482, 483] + list(range(801, 826))
            chapter_num = int(chapter)
            if chapter_num == 813:
                if ChargeClassifier._is_dimissed(disposition):
                    question_string = "Was the charge dismissed pursuant to a court-ordered diversion program?"
                    options = {"Yes": DivertedDuii(), "No": DismissedCharge()}
                    return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)
                else:
                    return AmbiguousChargeTypeWithQuestion([Duii()])
            if chapter_num in statute_range:
                if "felony" in level or "misdemeanor" in level:
                    if ChargeClassifier._is_dimissed(disposition):
                        return AmbiguousChargeTypeWithQuestion([DismissedCharge()])
                    else:
                        return AmbiguousChargeTypeWithQuestion([TrafficOffense()])
                else:
                    return AmbiguousChargeTypeWithQuestion([TrafficViolation()])
        if name == "pedestrian j-walking":
            return AmbiguousChargeTypeWithQuestion([TrafficViolation()])
        if "infraction" in level:
            return AmbiguousChargeTypeWithQuestion([TrafficViolation()])

    @staticmethod
    def _contempt_of_court(name):
        if "contempt" in name:
            # Build nested question tree bottom-up
            question_3_string = "Did this contempt of court proceeding arise from a criminal case in which a family member or member of your household was the legal victim?"
            question_3 = Question(
                question_3_string,
                question_3_string,
                {
                    "Yes": Answer(edit={"charge_type": SevereContemptOfCourt.__name__}),
                    "No": Answer(edit={"charge_type": ContemptOfCourt.__name__}),
                },
            )

            question_2_string = "Was this contempt of court proceeding initiated after someone said you violated a restraining order, stalking order, or no contact order?"
            question_2 = Question(
                question_2_string,
                question_2_string,
                {
                    "Yes": Answer(edit={"charge_type": ContemptOfCourt.__name__}),
                    "No": Answer(question=question_3),
                },
            )

            question_1_string = "Was this contempt of court proceeding initiated for failure to pay child support?"
            question_1 = Question(
                question_1_string,
                question_1_string,
                {
                    "Yes": Answer(edit={"charge_type": ContemptOfCourt.__name__}),
                    "No": Answer(question=question_2),
                },
            )

            charge_types = [ContemptOfCourt(), SevereContemptOfCourt()]
            return AmbiguousChargeTypeWithQuestion(charge_types, question_1)

    @staticmethod
    def _civil_offense(statute, name):
        statute_range = range(1, 100)
        chapter = ChargeClassifier._build_chapter_for_civil_offense(statute)
        is_civil_chapter_range = (chapter and chapter.isdigit() and int(chapter) in statute_range) or (
            statute.isdigit() and int(statute) in statute_range
        )
        is_fugitive = "fugitive" in name
        extradition_states = [
            "/AL",
            "/AK",
            "/AS",
            "/AZ",
            "/AR",
            "/CA",
            "/CO",
            "/CT",
            "/DE",
            "/DC",
            "/FL",
            "/GA",
            "/GU",
            "/HI",
            "/ID",
            "/IL",
            "/IN",
            "/IA",
            "/KS",
            "/KY",
            "/LA",
            "/ME",
            "/MD",
            "/MA",
            "/MI",
            "/MN",
            "/MS",
            "/MO",
            "/MT",
            "/NE",
            "/NV",
            "/NH",
            "/NJ",
            "/NM",
            "/NY",
            "/NC",
            "/ND",
            "/MP",
            "/OH",
            "/OK",
            "/OR",
            "/PA",
            "/PR",
            "/RI",
            "/SC",
            "/SD",
            "/TN",
            "/TX",
            "/UT",
            "/VT",
            "/VI",
            "/VA",
            "/WA",
            "/WV",
            "/WI",
            "/WY",
        ]
        is_extradition = any([state.lower() == name[-3:] for state in extradition_states])
        if is_civil_chapter_range or is_fugitive or is_extradition:
            return AmbiguousChargeTypeWithQuestion([CivilOffense()])

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
    def _criminal_forfeiture(statute):
        if statute == "131582":
            return AmbiguousChargeTypeWithQuestion([CriminalForfeiture()])

    @staticmethod
    def _parking_ticket(violation_type):
        if "parking" in violation_type.lower():
            return AmbiguousChargeTypeWithQuestion([ParkingTicket()])

    @staticmethod
    def _fare_violation(name):
        if "fare violation" in name or "non-payment of fare" in name:
            return AmbiguousChargeTypeWithQuestion([FareViolation()])

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
            return AmbiguousChargeTypeWithQuestion([SexCrime()])
        elif statute in SexCrime.romeo_and_juliet_exceptions:
            question_string = """
            Select "No" if all of the following are true:
            1. Are you required to report as a sex offender?
            2. Do you have any charges that are not eligible for expungement?
            """
            options = {
                "Yes": RomeoAndJulietIneligibleSexCrime(),
                "No (Rare, contact michael@qiu-qiulaw.com)": RomeoAndJulietNMASexCrime(),
            }
            return ChargeClassifier._build_ambiguous_charge_type_with_question(question_string, options)

    # TODO: Deduplicate with charge.dismissed()
    @staticmethod
    def _is_dimissed(disposition: Disposition):
        return disposition.status in [
            DispositionStatus.NO_COMPLAINT,
            DispositionStatus.DISMISSED,
            DispositionStatus.DIVERTED,
        ]

    @staticmethod
    def _build_ambiguous_charge_type_with_question(
        question: str, options: Dict[str, ChargeType]
    ) -> AmbiguousChargeTypeWithQuestion:
        options_dict = {}
        charge_types = []
        for key, value in options.items():
            charge_types.append(value)
            options_dict[key] = Answer(edit={"charge_type": value.__class__.__name__})
        return AmbiguousChargeTypeWithQuestion(charge_types, Question(question, question, options_dict))
