import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.schedule_1_p_c_s import Schedule1PCS

from tests.factories.charge_factory import ChargeFactory
from expungeservice.models.disposition import Disposition
from tests.models.test_charge import ChargeTypeTestsParent


class TestSingleChargeConvictionsSchedule1PCS(ChargeTypeTestsParent):

    """def setUp(self):
        ChargeTypeTestsParent.setUp(self)
        # Shouldn't need this.
    """

    def test_pcs_475854(self):
        self.charge_dict["name"] = "Unlawful possession of heroin"
        self.charge_dict["statute"] = "475.854"
        self.charge_dict["level"] = "Misdemeanor Class A"
        self.charge_dict["disposition"] = self.convicted
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(c)"

    def test_pcs_475874(self):
        self.charge_dict["name"] = "Unlawful possession of 3,4-methylenedioxymethamphetamine"
        self.charge_dict["statute"] = "475.874"
        self.charge_dict["level"] = "Misdemeanor Class A"
        self.charge_dict["disposition"] = self.convicted
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(c)"

    def test_pcs_475884(self):
        self.charge_dict["name"] = "Unlawful possession of cocaine"
        self.charge_dict["statute"] = "475.884"
        self.charge_dict["level"] = "Misdemeanor Class A"
        self.charge_dict["disposition"] = self.convicted
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(c)"

    def test_pcs_475894(self):
        self.charge_dict["name"] = "Unlawful possession of methamphetamine"
        self.charge_dict["statute"] = "475.894"
        self.charge_dict["level"] = "Misdemeanor Class A"
        self.charge_dict["disposition"] = self.convicted
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(c)"

    def test_pcs_475992(self):
        self.charge_dict["name"] = "Poss Controlled Sub 2"
        self.charge_dict["statute"] = "4759924B"
        self.charge_dict["level"] = "Felony Class C"
        self.charge_dict["disposition"] = self.convicted
        pcs_charge = self.create_recent_charge()
        self.charges.append(pcs_charge)

        assert isinstance(pcs_charge, Schedule1PCS)
        assert pcs_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert pcs_charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(c)"
