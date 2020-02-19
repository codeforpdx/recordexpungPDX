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
from expungeservice.models.charge_types.person_crime import FelonyClassBPersonCrime
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
        yield from ChargeClassifier._classification_by_level(self.level, self.statute)
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
        yield ChargeClassifier._subsection_6(section)
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
    def _subsection_6(section):
        conditionally_ineligible_statutes = [
            "163200",  #  (Criminal mistreatment in the second degree) if the victim at the time of the crime was 65 years of age or older.
            "163205",  # (overrides subsection 12.(Criminal mistreatment in the first degree) if the victim at the time of the crime was 65 years of age or older, or when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions).
            "163575",  #  (Endangering the welfare of a minor) (1)(a), when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions).
            "163145",  # (Criminally negligent homicide), when that offense was punishable as a Class C felony.
            "163165",  # ( ineligible if under subection(1)(h) ; Assault in the third degree of a minor 10 years or younger)
        ]
        if section in conditionally_ineligible_statutes:
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
            if ChargeClassifier._crime_against_person(statute):
                return FelonyClassBPersonCrime
            else:
                return FelonyClassB

    @staticmethod
    def _felony_class_a(level):
        if level == "Felony Class A":
            return FelonyClassA

    @staticmethod
    def _crime_against_person(statute):
        person_crime_statutes = [
            "97981",  # Purchase or Sale of a Body Part for Transplantation or Therapy;
            "97982",  # Alteration of a Document of Gift;
            # "162165",  # Escape I;
            # "162185",  # Supplying Contraband as defined in Crime Categories 6 and 7 (OAR 213-018-0070(1) and (2));
            "163095",  # Aggravated Murder;
            "163115",  # Murder II;
            "163115",  # Felony Murder;
            "163118",  # Manslaughter I;
            "163125",  # Manslaughter II;
            # "163145",  # Negligent Homicide;
            "163149",  # Aggravated Vehicular Homicide;
            "1631603",  # Felony Assault;
            # "163165",  # Assault III;
            # "163175",  # Assault II;
            "163185",  # Assault I;
            "1631874",  # Felony Strangulation;
            "163192",  # Endangering Person Protected by FAPA Order;
            "163196",  # Aggravated Driving While Suspended or Revoked;
            # "163205",  # Criminal Mistreatment I;
            "163207",  # Female Genital Mutilation;
            "163208",  # Assaulting a Public Safety Officer;
            "163213",  # Use of Stun Gun, Tear Gas, Mace I;
            # "163225",  # Kidnapping II;
            "163235",  # Kidnapping I;
            "163263",  # Subjecting Another Person to Involuntary Servitude II;
            "163264",  # Subjecting Another Person to Involuntary Servitude I;
            "163266",  # Trafficking in Persons;
            # "163275",  # Coercion as defined in Crime Category 7 (OAR 213-018-0035(1));
            "163355",  # Rape III;
            "163365",  # Rape II;
            "163375",  # Rape I;
            "163385",  # Sodomy III;
            "163395",  # Sodomy II;
            "163405",  # Sodomy I;
            "163408",  # Sexual Penetration II;
            "163411",  # Sexual Penetration I;
            "163413",  # Purchasing Sex With a Minor;
            "163425",  # Sexual Abuse II;
            "163427",  # Sexual Abuse I;
            "163432",  # Online Sexual Corruption of a Child II;
            "163433",  # Online Sexual Corruption of a Child I;
            "163452",  # Custodial Sexual Misconduct in the First Degree;
            "163465",  # Felony Public Indecency;
            "163472",  # Unlawful Dissemination of Intimate Image;
            "163479",  # Unlawful Contact with a Child;
            # "163525",  # Incest;
            # "163535",  # Abandon Child;
            "163537",  # Buying/Selling Custody of a Minor;
            "163547",  # Child Neglect I;
            "163670",  # Using Child In Display of Sexual Conduct;
            "163684",  # Encouraging Child Sex Abuse I;
            "163686",  # Encouraging Child Sex Abuse II;
            "163688",  # Possession of Material Depicting Sexually Explicit Conduct of Child I;
            "163689",  # Possession of Material Depicting Sexually Explicit Conduct of Child II;
            "163701",  # Invasion of Personal Privacy I;
            "163732",  # Stalking;
            "163750",  # Violation of Court's Stalking Order;
            "164075",  # Extortion as defined in Crime Category 7 (OAR 213-018-0075(1));
            "164225",  # Burglary I as defined in Crime Categories 8 and 9 (OAR 213-018-0025(1) and (2));
            "164325",  # Arson I;
            "164342",  # Arson Incident to the Manufacture of a Controlled Substance I;
            "1643772C",  # Computer Crime—Theft of an Intimate Image;
            # "164395",  # Robbery III;
            # "164405",  # Robbery II;
            "164415",  # Robbery I;
            "1648863",  # Tree Spiking (Injury);
            "166070",  # Aggravated Harassment;
            "166087",  # Abuse of Corpse I;
            # "166165",  # Bias Crime I;
            # "166220",  # Unlawful Use of a Weapon;
            "166275",  # Inmate In Possession of Weapon;
            "1663853",  # Felony Possession of a Hoax Destructive Device;
            "166643",  # Unlawful Possession of Soft Body Armor as defined in Crime Category 6 (OAR 213-018-0090(1));
            "167012",  # Promoting Prostitution;
            "167017",  # Compelling Prostitution;
            "167057",  # Luring a Minor;
            "1673204",  # Felony Animal Abuse I;
            "167322",  # Aggravated Animal Abuse I;
            "468951",  # Environmental Endangerment;
            "4757526A",  # Manufacturing or Delivering a Schedule IV Controlled Substance Thereby Causing Death to a Person;
            "475908",  # Causing Another to Ingest a Controlled Substance as defined in Crime Categories 8 and 9 (OAR 213-019-0007 and 0008);
            "475910",  # Unlawful Administration of a Controlled Substance as defined in Crime Categories 5, 8, and 9 (OAR 213-019-0007, -0008, and -0011);
            # "475B359",  # Arson Incident to Manufacture of Cannabinoid Extract I;
            # "475B367",  # Causing Another Person to Ingest Marijuana;
            # "475B371",  # Administration to Another Person Under 18 Years of Age;
            "6099903B",  # Maintaining Dangerous Dog;
            # "811705",  # Hit and Run Vehicle (Injury);
            # "8130105",  # Felony Driving Under the Influence of Intoxicants (as provided in OAR 213-004-0009);
            "8304752",  # Hit and Run Boat;
            "8373652B",  # Unlawful Operation of Weaponized Unmanned Aircraft System;
            "8373652C",  # Unlawful Operation of Weaponized Unmanned Aircraft System;
        ]
        if statute in person_crime_statutes:
            return True
