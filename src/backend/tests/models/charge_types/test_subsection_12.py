from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.subsection_12 import Subsection12
from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTest, Dispositions


class TestSubsection12(ChargeTypeTest):
    def test_subsection_12_dismissed(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Abandonment of a child"
        self.charge_dict["statute"] = "163.535"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.DISMISSED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert (
            subsection_12_charge.expungement_result.type_eligibility.reason == "Dismissal eligible under 137.225(1)(b)"
        )

    def test_subsection_12_163535(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Abandonment of a child"
        self.charge_dict["statute"] = "163.535"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert (
            subsection_12_charge.expungement_result.type_eligibility.reason
            == "Eligible under 137.225(12). This subsection is interpreted to override any conflicting subsections."
        )

    def test_subsection_12_163175(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Assault in the second degree"
        self.charge_dict["statute"] = "163.175"
        self.charge_dict["level"] = "Felony Class B"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    def test_subsection_12_163165(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Assault in the third degree"
        self.charge_dict["statute"] = "163.165"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    def test_subsection_12_163275(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Coercion"
        self.charge_dict["statute"] = "163.275"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    def test_subsection_12_163205(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Criminal mistreatment in the first degree"
        self.charge_dict["statute"] = "163.205"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    def test_subsection_12_162165(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Escape in the first degree"
        self.charge_dict["statute"] = "162.165"
        self.charge_dict["level"] = "Felony Class B"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    def test_subsection_12_163525(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Incest"
        self.charge_dict["statute"] = "163.525"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)
        assert subsection_12_charge.expungement_result.type_eligibility.status is EligibilityStatus.NEEDS_MORE_ANALYSIS
        assert (
            subsection_12_charge.expungement_result.type_eligibility.reason
            == "Incest is possibly eligible under 137.225(12), if the victim was at least 18 years of age."
        )

    def test_subsection_12_166165(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Intimidation in the first degree"
        self.charge_dict["statute"] = "166.165"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    def test_subsection_12_163225(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Kidnapping in the second degree"
        self.charge_dict["statute"] = "163.225"
        self.charge_dict["level"] = "Felony Class B"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    def test_subsection_12_164405(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Robbery in the second degree"
        self.charge_dict["statute"] = "164.405"
        self.charge_dict["level"] = "Felony Class B"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    def test_subsection_12_164395(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Robbery in the third degree"
        self.charge_dict["statute"] = "164.395"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    def test_subsection_12_162185(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Supplying contraband"
        self.charge_dict["statute"] = "162.185"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    def test_subsection_12_166220(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Unlawful use of weapon"
        self.charge_dict["statute"] = "166.220"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)

    # Test sub-chapters are not compared when not necessary.
    def test_subsection_12_charge_that_includes_sub_chapter(self):
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["name"] = "Unlawful use of weapon"
        self.charge_dict["statute"] = "166.220(1)(b)"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = Dispositions.CONVICTED
        subsection_12_charge = ChargeFactory.create(**self.charge_dict)

        assert isinstance(subsection_12_charge, Subsection12)
