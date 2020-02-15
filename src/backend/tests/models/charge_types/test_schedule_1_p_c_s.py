import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.schedule_1_p_c_s import Schedule1PCS

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition


class TestSingleChargeConvictionsSchedule1PCS(unittest.TestCase):
    def setUp(self):
        last_week = datetime.today() - timedelta(days=7)
        self.single_charge = ChargeFactory.build(disposition=Disposition(ruling="Convicted", date=last_week))
        self.charges = []

    def create_recent_charge(self):
        charge = ChargeFactory.save(self.single_charge)
        return charge

    # Possession of controlled substance tests

    def test_pcs_475854(self):
        self.single_charge["name"] = "Unlawful possession of heroin"
        self.single_charge["statute"] = "475.854"
        self.single_charge["level"] = "Misdemeanor Class A"
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.type_name == "Schedule 1 PCS"
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(C)"

    def test_pcs_475874(self):
        self.single_charge["name"] = "Unlawful possession of 3,4-methylenedioxymethamphetamine"
        self.single_charge["statute"] = "475.874"
        self.single_charge["level"] = "Misdemeanor Class A"
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.type_name == "Schedule 1 PCS"
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(C)"

    def test_pcs_475884(self):
        self.single_charge["name"] = "Unlawful possession of cocaine"
        self.single_charge["statute"] = "475.884"
        self.single_charge["level"] = "Misdemeanor Class A"
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.type_name == "Schedule 1 PCS"
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(C)"

    def test_pcs_475894(self):
        self.single_charge["name"] = "Unlawful possession of methamphetamine"
        self.single_charge["statute"] = "475.894"
        self.single_charge["level"] = "Misdemeanor Class A"
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.type_name == "Schedule 1 PCS"
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(C)"

    def test_pcs_475992(self):
        self.single_charge["name"] = "Poss Controlled Sub 2"
        self.single_charge["statute"] = "4759924B"
        self.single_charge["level"] = "Felony Class C"
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.type_name == "Schedule 1 PCS"
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(C)"
