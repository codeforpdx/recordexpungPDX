import unittest
from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.subsection_6 import Subsection6
from expungeservice.models.disposition import Disposition

from tests.factories.charge_factory import ChargeFactory
from tests.factories.case_factory import CaseFactory


class TestSubsection6(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.dismissal = Disposition(ruling="Dismissed", date=last_week)
        self.charge_dict = ChargeFactory.default_dict()
        self.charge_dict["disposition"] = Disposition(ruling="Convicted", date=last_week)

    def create_recent_charge(self):
        return ChargeFactory.create(**self.charge_dict)

    def test_subsection_6_dismissed(self):
        self.charge_dict["name"] = "Criminal mistreatment in the second degree"
        self.charge_dict["statute"] = "163.200"
        self.charge_dict["level"] = "Misdemeanor Class A"
        self.charge_dict["disposition"] = self.dismissal

        subsection_6_charge = self.create_recent_charge()

        assert isinstance(subsection_6_charge, Subsection6)
        assert subsection_6_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert (
            subsection_6_charge.expungement_result.type_eligibility.reason == "Dismissal eligible under 137.225(1)(b)"
        )

    def test_subsection_6_163200(self):
        self.charge_dict["name"] = "Criminal mistreatment in the second degree"
        self.charge_dict["statute"] = "163.200"
        self.charge_dict["level"] = "Misdemeanor Class A"
        subsection_6_charge = self.create_recent_charge()

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
        subsection_6_charge = self.create_recent_charge()

        assert isinstance(subsection_6_charge, Subsection6)

    def test_subsection_6_163145(self):
        self.charge_dict["name"] = "Criminally negligent homicide"
        self.charge_dict["statute"] = "163.145"
        self.charge_dict["level"] = "Felony Class B"
        subsection_6_charge = self.create_recent_charge()

        assert isinstance(subsection_6_charge, Subsection6)
