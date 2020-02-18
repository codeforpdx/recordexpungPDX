import unittest

from datetime import datetime, timedelta

from expungeservice.models.charge_types.felony_class_a import FelonyClassA
from expungeservice.models.disposition import Disposition
from expungeservice.models.expungement_result import EligibilityStatus

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTest


class TestSingleChargeConvictionsFelonyClassA(ChargeTypeTest):
    def test_felony_class_a_charge(self):
        self.charge_dict["name"] = "Assault in the first degree"
        self.charge_dict["statute"] = "163.185"
        self.charge_dict["level"] = "Felony Class A"
        self.charge_dict["disposition"] = self.convicted
        felony_class_a_convicted = self.create_recent_charge()
        self.charges.append(felony_class_a_convicted)

        assert isinstance(felony_class_a_convicted, FelonyClassA)
        assert felony_class_a_convicted.expungement_result.type_eligibility.status is EligibilityStatus.INELIGIBLE
        assert (
            felony_class_a_convicted.expungement_result.type_eligibility.reason == "Ineligible by omission from statute"
        )

    def test_felony_class_a_dismissed(self):
        self.charge_dict["name"] = "Assault in the first degree"
        self.charge_dict["statute"] = "163.185"
        self.charge_dict["level"] = "Felony Class A"
        self.charge_dict["disposition"] = self.dismissed
        felony_class_a_dismissed = self.create_recent_charge()
        self.charges.append(felony_class_a_dismissed)

        assert isinstance(felony_class_a_dismissed, FelonyClassA)
        assert felony_class_a_dismissed.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert (
            felony_class_a_dismissed.expungement_result.type_eligibility.reason
            == "Dismissals are eligible under 137.225(1)(b)"
        )

    def test_felony_class_a_no_complaint(self):
        self.charge_dict["disposition"] = self.no_complaint
        self.charge_dict["name"] = "Assault in the first degree"
        self.charge_dict["statute"] = "163.185"
        self.charge_dict["level"] = "Felony Class A"
        felony_class_a_no_complaint = self.create_recent_charge()
        self.charges.append(felony_class_a_no_complaint)

        assert isinstance(felony_class_a_no_complaint, FelonyClassA)
        assert felony_class_a_no_complaint.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert (
            felony_class_a_no_complaint.expungement_result.type_eligibility.reason
            == "Dismissals are eligible under 137.225(1)(b)"
        )
