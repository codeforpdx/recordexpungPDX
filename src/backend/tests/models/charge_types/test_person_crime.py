from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.person_crime import PersonCrime
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTest, Dispositions


class TestSingleChargeConvictionsPersonCrime(ChargeTypeTest):
    def test_misdemeanor_sex_crime(self):
        charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
        charge_dict["name"] = "Sexual Abuse in the Third Degree"
        charge_dict["statute"] = "163.415"
        charge_dict["level"] = "Misdemeanor Class A"
        charge_dict["disposition"] = Dispositions.CONVICTED
        misdemeanor_class_a_convicted = ChargeFactory.create(**charge_dict)

        assert isinstance(misdemeanor_class_a_convicted, PersonCrime)
        assert misdemeanor_class_a_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert misdemeanor_class_a_convicted.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"

    def test_min_statute_range_for_crimes_against_persons(self):
        charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
        charge_dict["statute"] = "163.305"
        convicted_charge = ChargeFactory.create(**charge_dict)

        assert isinstance(convicted_charge, PersonCrime)
        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"

    def test_max_statute_range_for_crimes_against_persons(self):
        charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
        charge_dict["statute"] = "163.479"
        convicted_charge = ChargeFactory.create(**charge_dict)

        assert isinstance(convicted_charge, PersonCrime)
        assert convicted_charge.type_name == "Person Crime"
        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"

    def test_min_statute_range_for_other_crimes_against_persons(self):
        charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
        charge_dict["statute"] = "163.670"
        convicted_charge = ChargeFactory.create(**charge_dict)

        assert isinstance(convicted_charge, PersonCrime)
        assert convicted_charge.type_name == "Person Crime"
        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"

    def test_max_statute_range_for_other_crimes_against_persons(self):
        charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
        charge_dict["statute"] = "163.693"
        convicted_charge = ChargeFactory.create(**charge_dict)

        assert isinstance(convicted_charge, PersonCrime)
        assert convicted_charge.type_name == "Person Crime"
        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"

    def test_min_statute_range_for_promoting_prostitution(self):
        charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
        charge_dict["statute"] = "167.008"
        convicted_charge = ChargeFactory.create(**charge_dict)

        assert isinstance(convicted_charge, PersonCrime)
        assert convicted_charge.type_name == "Person Crime"
        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"

    def test_max_statute_range_for_promoting_prostitution(self):
        charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
        charge_dict["statute"] = "167.107"
        convicted_charge = ChargeFactory.create(**charge_dict)

        assert isinstance(convicted_charge, PersonCrime)
        assert convicted_charge.type_name == "Person Crime"
        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"

    def test_min_statute_range_for_obscenity_and_minors(self):
        charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
        charge_dict["statute"] = "167.057"
        convicted_charge = ChargeFactory.create(**charge_dict)

        assert isinstance(convicted_charge, PersonCrime)
        assert convicted_charge.type_name == "Person Crime"
        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"

    def test_max_statute_range_for_obscenity_and_minors(self):
        charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
        charge_dict["statute"] = "167.080"
        convicted_charge = ChargeFactory.create(**charge_dict)

        assert isinstance(convicted_charge, PersonCrime)
        assert convicted_charge.type_name == "Person Crime"
        assert convicted_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert convicted_charge.expungement_result.type_eligibility.reason == "Ineligible under 137.225(5)"

    def test_rape_class_c_felony(self):
        charge_dict = ChargeFactory.default_dict(disposition=Dispositions.CONVICTED)
        charge_dict["name"] = "Rape in the Third Degree"
        charge_dict["statute"] = "163.355"
        charge_dict["level"] = "Felony Class C"
        sex_crime_charge = ChargeFactory.create(**charge_dict)

        assert isinstance(sex_crime_charge, PersonCrime)
        assert sex_crime_charge.type_name == "Person Crime"
        assert sex_crime_charge.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
