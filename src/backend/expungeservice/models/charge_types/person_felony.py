from dataclasses import dataclass
from typing import List

from expungeservice.models.charge import ChargeType
from expungeservice.models.charge import ChargeUtil
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(frozen=True)
class PersonFelonyClassB(ChargeType):
    type_name: str = "Person Felony Class B"
    expungement_rules: str = (
        """If a [Class B Felony](#FelonyClassB) is also defined as a person felony under Oregon law, it is type-ineligible.
A person felony is defined in section 14 of this page: (https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=712)
Dismissal of a person felony is eligible as usual under 137.225(1)(b).
A person felony that is below a class B felony is not considered under this subsection and lower levels of charge may still be eligible, with the exceptions named elsewhere such as in [Subsection 6](#Subsection6).
"""
    )
    """
    Some statutes listed in the definition for person crime only apply to a particular subsection.
    """
    statutes_with_subsection = [
        "1631874",  # [contains subsection] # Felony Strangulation; class C felony
        "1643772C",  # [contains subsection] # Computer Crime—Theft of an Intimate Image; class C misdemeanor
        "1648863",  # [contains subsection] # Tree Spiking (Injury); class B felony
        "1663853",  # [contains subsection] # Felony Possession of a Hoax Destructive Device; class C felony
        "1673204",  # [contains subsection] # Felony Animal Abuse I; class C felony
        "4757526A",  # [contains subsection] # Manufacturing or Delivering a Schedule IV Controlled Substance Thereby Causing Death to a Person; adjacent to a class B felony
        "6099903B",  # [contains subsection] # Maintaining Dangerous Dog; class C felony
        "8304752",  # [contains subsection] # Hit and Run Boat; no level
        "8373652B",  # [contains subsection] # Unlawful Operation of Weaponized Unmanned Aircraft System; class C felony
        "8373652C",  # [contains subsection] # Unlawful Operation of Weaponized Unmanned Aircraft System; class B felony
    ]
    """
    This list is the exhaustive set of statutes named under the Person Felony definition https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=712
    Commented lines in this list are either included above (in which case the line is marked with "[contains subsection]"), or are classified as a different charge type such as Sex Crime.
    """
    statutes = [
        "97981",  # Purchase or Sale of a Body Part for Transplantation or Therapy;
        "97982",  # Alteration of a Document of Gift;
        "162165",  # Escape I;
        "162185",  # Supplying Contraband as defined in Crime Categories 6 and 7 (OAR 213-018-0070(1) and (2));
        "163095",  # Aggravated Murder;
        "163115",  # Murder II;
        "163115",  # Felony Murder;
        "163118",  # Manslaughter I;
        "163125",  # Manslaughter II;
        "163145",  # [Subsection 6] Negligent Homicide;
        "163149",  # Aggravated Vehicular Homicide;
        # "1631603", # [contains subsection] # Felony Assault;
        "163165",  # [Subsection 6] Assault III;
        "163175",  # Assault II;
        "163185",  # Assault I;
        # "1631874", # [contains subsection] # Felony Strangulation;
        "163192",  # Endangering Person Protected by FAPA Order;
        "163196",  # Aggravated Driving While Suspended or Revoked;
        "163205",  # [Subsection 6]  Criminal Mistreatment I;
        "163207",  # Female Genital Mutilation;
        "163208",  # Assaulting a Public Safety Officer;
        "163213",  # Use of Stun Gun, Tear Gas, Mace I;
        "163225",  # Kidnapping II;
        "163235",  # Kidnapping I;
        "163263",  # Subjecting Another Person to Involuntary Servitude II;
        "163264",  # Subjecting Another Person to Involuntary Servitude I;
        "163266",  # Trafficking in Persons;
        "163275",  # Coercion as defined in Crime Category 7 (OAR 213-018-0035(1));
        # "163355",  # [Sex Crime] Rape III;
        # "163365",  # [Sex Crime] Rape II;
        # "163375",  # [Sex Crime] Rape I;
        # "163385",  # [Sex Crime] Sodomy III;
        # "163395",  # [Sex Crime] Sodomy II;
        # "163405",  # [Sex Crime] Sodomy I;
        # "163408",  # [Sex Crime] Sexual Penetration II;
        # "163411",  # [Sex Crime] Sexual Penetration I;
        # "163413",  # [Sex Crime] Purchasing Sex With a Minor;
        # "163425",  # [Sex Crime] Sexual Abuse II;
        # "163427",  # [Sex Crime] Sexual Abuse I;
        # "163432",  # [Sex Crime] Online Sexual Corruption of a Child II;
        # "163433",  # [Sex Crime] Online Sexual Corruption of a Child I;
        # "163452",  # [Sex Crime] Custodial Sexual Misconduct in the First Degree;
        # "163465",  # [Sex Crime] Felony Public Indecency;
        # "163472",  # [Sex Crime] Unlawful Dissemination of Intimate Image;
        # "163479",  # [Sex Crime] Unlawful Contact with a Child;
        "163525",  # Incest;
        "163535",  # Abandon Child;
        "163537",  # Buying/Selling Custody of a Minor;
        "163547",  # Child Neglect I;
        # "163670",  # [Sex Crime] Using Child In Display of Sexual Conduct;
        # "163684",  # [Sex Crime] Encouraging Child Sex Abuse I;
        # "163686",  # [Sex Crime] Encouraging Child Sex Abuse II;
        # "163688",  # [Sex Crime] Possession of Material Depicting Sexually Explicit Conduct of Child I;
        # "163689",  # [Sex Crime] Possession of Material Depicting Sexually Explicit Conduct of Child II;
        "163701",  # Invasion of Personal Privacy I;
        "163732",  # Stalking;
        "163750",  # Violation of Court's Stalking Order;
        "164075",  # Extortion as defined in Crime Category 7 (OAR 213-018-0075(1));
        "164225",  # Burglary I as defined in Crime Categories 8 and 9 (OAR 213-018-0025(1) and (2));
        "164325",  # Arson I;
        "164342",  # Arson Incident to the Manufacture of a Controlled Substance I;
        # "1643772C", # [contains subsection] # Computer Crime—Theft of an Intimate Image;
        "164395",  # Robbery III;
        "164405",  # Robbery II;
        "164415",  # Robbery I;
        # "1648863", # [contains subsection] # Tree Spiking (Injury);
        "166070",  # Aggravated Harassment;
        "166087",  # Abuse of Corpse I;
        "166165",  # Bias Crime I;
        "166220",  # Unlawful Use of a Weapon;
        # "166275",  # Inmate In Possession of Weapon; # Handled separately in charge classifier
        # "1663853", # [contains subsection] # Felony Possession of a Hoax Destructive Device;
        "166643",  # Unlawful Possession of Soft Body Armor as defined in Crime Category 6 (OAR 213-018-0090(1));
        # "167012",  # [Sex Crimes] Promoting Prostitution;
        # "167017",  # [Sex Crimes] Compelling Prostitution;
        # "167057",  # [Sex Crimes] Luring a Minor;
        # "1673204", # [contains subsection] # Felony Animal Abuse I;
        "167322",  # Aggravated Animal Abuse I;
        "468951",  # Environmental Endangerment;
        # "4757526A", # [contains subsection] # Manufacturing or Delivering a Schedule IV Controlled Substance Thereby Causing Death to a Person;
        "475908",  # Causing Another to Ingest a Controlled Substance as defined in Crime Categories 8 and 9 (OAR 213-019-0007 and 0008);
        "475910",  # Unlawful Administration of a Controlled Substance as defined in Crime Categories 5, 8, and 9 (OAR 213-019-0007, -0008, and -0011);
        # "475B359",  # [Marijuana Ineligible] Arson Incident to Manufacture of Cannabinoid Extract I;
        # "475B367",  # [Marijuana Ineligible] Causing Another Person to Ingest Marijuana;
        # "475B371",  # [Marijuana Ineligible] Administration to Another Person Under 18 Years of Age;
        # "6099903B", # [contains subsection] # Maintaining Dangerous Dog;
        # "811705",  # [traffic offense] Hit and Run Vehicle (Injury);
        # "8130105", # [traffic offense] Felony Driving Under the Influence of Intoxicants (as provided in OAR 213-004-0009);
        # "8304752", # [contains subsection] # Hit and Run Boat;
        # "8373652B", # [contains subsection] # Unlawful Operation of Weaponized Unmanned Aircraft System;
        # "8373652C", # [contains subsection] # Unlawful Operation of Weaponized Unmanned Aircraft System;
    ]

    def type_eligibility(self, disposition):
        if ChargeUtil.dismissed(disposition):
            raise ValueError("Dismissed criminal charges should have been caught by another class.")
        elif ChargeUtil.convicted(disposition):
            return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(5)(a)")
