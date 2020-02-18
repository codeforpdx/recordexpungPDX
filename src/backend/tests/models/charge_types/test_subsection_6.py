from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.subsection_6 import Subsection6
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTest, Dispositions


class TestSubsection6(ChargeTypeTest):
    def setUp(self):
        super().setUp()
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["disposition"] = Dispositions.CONVICTED

    def test_subsection_6_dismissed(self):
        self.charge_dict["name"] = "Criminal mistreatment in the second degree"
        self.charge_dict["statute"] = "163.200"
        self.charge_dict["level"] = "Misdemeanor Class A"
        self.charge_dict["disposition"] = Dispositions.DISMISSED

        subsection_6_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_6_charge, Subsection6)
        assert subsection_6_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert (
            subsection_6_charge.expungement_result.type_eligibility.reason
            == "Dismissals are eligible under 137.225(1)(b)"
        )

    def test_subsection_6_163200(self):
        self.charge_dict["name"] = "Criminal mistreatment in the second degree"
        self.charge_dict["statute"] = "163.200"
        self.charge_dict["level"] = "Misdemeanor Class A"
        subsection_6_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_6_charge, Subsection6)
        assert subsection_6_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert (
            subsection_6_charge.expungement_result.type_eligibility.reason
            == "Ineligible under 137.225(6) in certain circumstances."
        )

    def test_subsection_6_163575(self):
        self.charge_dict["name"] = "Endangering the welfare of a minor"
        self.charge_dict["statute"] = "163.575"
        self.charge_dict["level"] = "Misdemeanor Class A"
        subsection_6_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_6_charge, Subsection6)

    def test_subsection_6_163145(self):
        self.charge_dict["name"] = "Criminally negligent homicide"
        self.charge_dict["statute"] = "163.145"
        self.charge_dict["level"] = "Felony Class B"
        subsection_6_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_6_charge, Subsection6)
