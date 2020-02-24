from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.person_crime import PersonCrime
from expungeservice.models.charge_types.felony_class_c import FelonyClassC
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import Dispositions
import pytest

person_crime_statutes = [
    "97981",  # Purchase or Sale of a Body Part for Transplantation or Therapy;
    "97982",  # Alteration of a Document of Gift;
    "162165",  # Escape I;
    "162185",  # Supplying Contraband as defined in Crime Categories 6 and 7 (OAR 213-018-0070(1) and (2));
    "163095",  # Aggravated Murder;
    "163115",  # Murder II;
    "163115",  # Felony Murder;
    "163118",  # Manslaughter I;
    "163125",  # Manslaughter II;
    "163145",  # Negligent Homicide;
    "163149",  # Aggravated Vehicular Homicide;
    "1631603",  # Felony Assault;
    "163165",  # Assault III;
    "163175",  # Assault II;
    "163185",  # Assault I;
    "1631874",  # Felony Strangulation;
    "163192",  # Endangering Person Protected by FAPA Order;
    "163196",  # Aggravated Driving While Suspended or Revoked;
    "163205",  # Criminal Mistreatment I;
    "163207",  # Female Genital Mutilation;
    "163208",  # Assaulting a Public Safety Officer;
    "163213",  # Use of Stun Gun, Tear Gas, Mace I;
    "163225",  # Kidnapping II;
    "163235",  # Kidnapping I;
    "163263",  # Subjecting Another Person to Involuntary Servitude II;
    "163264",  # Subjecting Another Person to Involuntary Servitude I;
    "163266",  # Trafficking in Persons;
    "163275",  # Coercion as defined in Crime Category 7 (OAR 213-018-0035(1));
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
    "163525",  # Incest;
    "163535",  # Abandon Child;
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
    "164395",  # Robbery III;
    "164405",  # Robbery II;
    "164415",  # Robbery I;
    "1648863",  # Tree Spiking (Injury);
    "166070",  # Aggravated Harassment;
    "166087",  # Abuse of Corpse I;
    "166165",  # Bias Crime I;
    "166220",  # Unlawful Use of a Weapon;
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
    "475B359",  # Arson Incident to Manufacture of Cannabinoid Extract I;
    "475B367",  # Causing Another Person to Ingest Marijuana;
    "475B371",  # Administration to Another Person Under 18 Years of Age;
    "6099903B",  # Maintaining Dangerous Dog;
    "811705",  # Hit and Run Vehicle (Injury);
    "8130105",  # Felony Driving Under the Influence of Intoxicants (as provided in OAR 213-004-0009);
    "8304752",  # Hit and Run Boat;
    "8373652B",  # Unlawful Operation of Weaponized Unmanned Aircraft System;
    "8373652C",  # Unlawful Operation of Weaponized Unmanned Aircraft System;
]


@pytest.mark.parametrize("person_crime_statute", person_crime_statutes)
def test_felony_b_person_crimes(person_crime_statute):
    charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
    charge_dict["name"] = "Generic"
    charge_dict["statute"] = person_crime_statute
    charge_dict["level"] = "Felony Class B"
    charge_dict["disposition"] = Dispositions.CONVICTED
    person_crime_felony_class_b_convicted = ChargeFactory.create(**charge_dict)

    assert isinstance(person_crime_felony_class_b_convicted, PersonCrime)
    assert (
        person_crime_felony_class_b_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
    )
    assert (
        person_crime_felony_class_b_convicted.expungement_result.type_eligibility.reason
        == "Ineligible under 137.225(5)"
    )


# @pytest.mark.parametrize("person_crime_statute", person_crime_statutes)
# def test_felony_c_person_crimes(person_crime_statute):
#     charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
#     charge_dict["name"] = "Generic"
#     charge_dict["statute"] = person_crime_statute
#     charge_dict["level"] = "Felony Class C"
#     charge_dict["disposition"] = Dispositions.CONVICTED
#     person_crime_felony_class_c_convicted = ChargeFactory.create(**charge_dict)
#
#     assert isinstance(person_crime_felony_class_c_convicted, FelonyClassC)
#     assert person_crime_felony_class_c_convicted.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
#     assert person_crime_felony_class_c_convicted.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"
