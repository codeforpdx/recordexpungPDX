from dataclasses import dataclass
from typing import List

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class PersonFelonyClassB(Charge):
    type_name: str = "Person Felony Class B"
    expungement_rules: str = (
        """If a [Class B Felony](#FelonyClassB) is also defined as a person felony under Oregon law, it is type-ineligible.
A person felony is defined in section 14 of this page: (https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=712)
In some cases, the statute named in this list includes a subsection. Because OECI can have a data error that excludes the subsection, records that are a B felony and also charged under one of these sections are tagged with Needs More Analysis, because the charge may or may not constitute a person felony depending on the subsection under which the person was charged.
Dismissal of a person felony is eligible as usual under 137.225(1)(b).
A person felony that is not a class B felony is not considered under this subsection and lower levels of charge may still be eligible, with the exceptions named elsewhere such as in [Subsection 12](#Subsection12).
"""
    )

    """Some statutes listed in the definition for person crime include a subsection which need special logic to handle potential OECI errors"""
    statutes_with_subsection = [
        "1631603",  # [contains subsection] # Felony Assault; class C felony
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
    Commented lines in this list are either included above (in which case the line is marked with "[contains subsection]"), or are classified as a different charge type such as Sex Crime or Subsection 12.
    """
    statutes = [
        "97981",  # Purchase or Sale of a Body Part for Transplantation or Therapy;
        "97982",  # Alteration of a Document of Gift;
        # "162165",  # Escape I;
        # "162185",  # Supplying Contraband as defined in Crime Categories 6 and 7 (OAR 213-018-0070(1) and (2));
        "163095",  # Aggravated Murder;
        "163115",  # Murder II;
        "163115",  # Felony Murder;
        "163118",  # Manslaughter I;
        "163125",  # Manslaughter II;
        "163145",  # Negligent Homicide;
        "163149",  # Aggravated Vehicular Homicide;
        # "1631603", # [contains subsection] # Felony Assault;
        "163165",  # Assault III;
        # "163175",  # Assault II;
        "163185",  # Assault I;
        # "1631874", # [contains subsection] # Felony Strangulation;
        "163192",  # Endangering Person Protected by FAPA Order;
        "163196",  # Aggravated Driving While Suspended or Revoked;
        "163205",  # Criminal Mistreatment I;
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
        # "1643772C", # [contains subsection] # Computer Crime—Theft of an Intimate Image;
        # "164395",  # Robbery III;
        # "164405",  # Robbery II;
        "164415",  # Robbery I;
        # "1648863", # [contains subsection] # Tree Spiking (Injury);
        "166070",  # Aggravated Harassment;
        "166087",  # Abuse of Corpse I;
        # "166165",  # Bias Crime I;
        # "166220",  # Unlawful Use of a Weapon;
        "166275",  # Inmate In Possession of Weapon;
        # "1663853", # [contains subsection] # Felony Possession of a Hoax Destructive Device;
        "166643",  # Unlawful Possession of Soft Body Armor as defined in Crime Category 6 (OAR 213-018-0090(1));
        "167012",  # Promoting Prostitution;
        "167017",  # Compelling Prostitution;
        "167057",  # Luring a Minor;
        # "1673204", # [contains subsection] # Felony Animal Abuse I;
        "167322",  # Aggravated Animal Abuse I;
        "468951",  # Environmental Endangerment;
        # "4757526A", # [contains subsection] # Manufacturing or Delivering a Schedule IV Controlled Substance Thereby Causing Death to a Person;
        "475908",  # Causing Another to Ingest a Controlled Substance as defined in Crime Categories 8 and 9 (OAR 213-019-0007 and 0008);
        "475910",  # Unlawful Administration of a Controlled Substance as defined in Crime Categories 5, 8, and 9 (OAR 213-019-0007, -0008, and -0011);
        # "475B359",  # Arson Incident to Manufacture of Cannabinoid Extract I;
        # "475B367",  # Causing Another Person to Ingest Marijuana;
        # "475B371",  # Administration to Another Person Under 18 Years of Age;
        # "6099903B", # [contains subsection] # Maintaining Dangerous Dog;
        # "811705",  # Hit and Run Vehicle (Injury);
        # "8130105", # Felony Driving Under the Influence of Intoxicants (as provided in OAR 213-004-0009);
        # "8304752", # [contains subsection] # Hit and Run Boat;
        # "8373652B", # [contains subsection] # Unlawful Operation of Weaponized Unmanned Aircraft System;
        # "8373652C", # [contains subsection] # Unlawful Operation of Weaponized Unmanned Aircraft System;
    ]

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            if self.statute in [full_statute[:6] for full_statute in self.statutes_with_subsection]:
                return TypeEligibility(
                    EligibilityStatus.NEEDS_MORE_ANALYSIS,
                    reason="OECI may be missing a statute subsection which would make this charge a person crime, and thus ineligible under 137.225(5)(a)",
                )
            else:
                return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(5)(a)")


"""The following sections are defined in (ORS)[https://www.oregonlaws.org/] as class B felonies.
This list is not used directly to determine expungement eligibility because we instead use the charge level provided in the OECI record.
However, it's included here as additional information about the expected expungement behavior.
If the OECI data always matches the severity level in ORS, we would always see exactly these statutes tagged as a Person Felony Class B.
Some of these are only subsections which are a class B felony, while the full section is not.

"162165", # Escape I;
"163125", # Manslaughter II;
"163145", # Negligent Homicide;
"163175", # Assault II;
"163207", # Female Genital Mutilation;
"163225", # Kidnapping II;
"163264", # Subjecting Another Person to Involuntary Servitude I;
"1632661A", # Trafficking in Persons;
"1632662", # Trafficking in Persons;
"163365", # Rape II;
"163395", # Sodomy II;
"163408", # Sexual Penetration II;
"1634132B", # Purchasing Sex With a Minor;
"163427", # Sexual Abuse I;
"163433", # Online Sexual Corruption of a Child I;
"163537", # Buying/Selling Custody of a Minor;
"163547", # Child Neglect I;
"163684", # Encouraging Child Sex Abuse I;
"163688", # Possession of Material Depicting Sexually Explicit Conduct of Child I;
"164075", # Extortion as defined in Crime Category 7 (OAR 213-018-0075(1));
"164405", # Robbery II;
"1648863", # Tree Spiking (Injury);
"166087", # Abuse of Corpse I;
"166643", # Unlawful Possession of Soft Body Armor as defined in Crime Category 6 (OAR 213-018-0090(1));
"167017", # Compelling Prostitution;
"475908", # Causing Another to Ingest a Controlled Substance as defined in Crime Categories 8 and 9 (OAR 213-019-0007 and 0008);
"4759102", # Unlawful Administration of a Controlled Substance as defined in Crime Categories 5, 8, and 9 (OAR 213-019-0007, -0008, and -0011);
"475B3672B", # Causing Another Person to Ingest Marijuana;
"8117052B", # Hit and Run Vehicle (Injury);
"8373652C", # Unlawful Operation of Weaponized Unmanned Aircraft System;
"""
