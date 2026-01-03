"""
Tests for the 2026 Oregon expungement form filling logic.
"""

from datetime import datetime
from unittest.mock import Mock

from expungeservice.form_filling import CaseResults
from expungeservice.form_filling_2026 import PDFFieldMapper2026, get_pdf_filename, FormFilling2026
from expungeservice.models.case import Case
from expungeservice.models.charge import Charge, EditStatus
from expungeservice.models.charge_types.felony_class_b import FelonyClassB
from expungeservice.models.expungement_result import ChargeEligibilityStatus
from expungeservice.util import DateWithFuture


def create_date(y, m, d):
    return DateWithFuture.fromdatetime(datetime(y, m, d))


USER_DATA = {
    "full_name": "Test Person",
    "date_of_birth": "1/1/1990",
    "mailing_address": "123 Test St",
    "city": "Portland",
    "state": "OR",
    "zip_code": "97201",
    "phone_number": "555-555-1234",
}


def make_eligible_conviction(name="Theft", charge_id="case1-1"):
    """Create a mock eligible conviction charge."""
    charge = Mock(spec=Charge)
    charge.name = name
    charge.edit_status = EditStatus.UNCHANGED
    charge.date = create_date(2020, 1, 1)
    charge.ambiguous_charge_id = charge_id
    charge.charge_type = FelonyClassB()
    charge.disposition = Mock()
    charge.disposition.date = create_date(2020, 6, 1)
    charge.disposition.status = "Convicted"
    charge.expungement_result = Mock()
    charge.expungement_result.charge_eligibility = Mock()
    charge.expungement_result.charge_eligibility.status = ChargeEligibilityStatus.ELIGIBLE_NOW
    charge.convicted = Mock(return_value=True)
    charge.dismissed = Mock(return_value=False)
    charge.probation_revoked = False
    charge.no_complaint = Mock(return_value=False)
    return charge


def make_ineligible_conviction(name="Assault", charge_id="case1-2"):
    """Create a mock ineligible conviction charge."""
    charge = make_eligible_conviction(name, charge_id)
    charge.expungement_result.charge_eligibility.status = ChargeEligibilityStatus.INELIGIBLE
    return charge


def make_eligible_dismissal(name="Trespass", charge_id="case1-3"):
    """Create a mock eligible dismissed charge."""
    charge = Mock(spec=Charge)
    charge.name = name
    charge.edit_status = EditStatus.UNCHANGED
    charge.date = create_date(2020, 1, 1)
    charge.ambiguous_charge_id = charge_id
    charge.charge_type = Mock()
    charge.disposition = Mock()
    charge.disposition.date = create_date(2020, 3, 1)
    charge.disposition.status = "Dismissed"
    charge.expungement_result = Mock()
    charge.expungement_result.charge_eligibility = Mock()
    charge.expungement_result.charge_eligibility.status = ChargeEligibilityStatus.ELIGIBLE_NOW
    charge.convicted = Mock(return_value=False)
    charge.dismissed = Mock(return_value=True)
    charge.probation_revoked = False
    charge.no_complaint = Mock(return_value=False)
    return charge


def make_case(charges, county="Washington", case_number="123456"):
    """Create a mock case with the given charges."""
    case = Mock(spec=Case)
    case.charges = charges
    case.summary = Mock()
    case.summary.location = county
    case.summary.case_number = case_number
    case.summary.name = "TEST PERSON"
    case.summary.balance_due_in_cents = 0
    case.summary.district_attorney_number = "DA123"
    case.summary.sid = "SID123"
    return case


class TestPDFFieldMapper2026OptionSelection:
    """Test that the correct option checkboxes are selected."""

    def test_full_conviction_expungement_selects_option_1_all_charges(self):
        """When all convictions are eligible, select Option 1 with 'all charges'."""
        charges = [make_eligible_conviction("Theft", "case1-1")]
        case = make_case(charges)
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        mapper = PDFFieldMapper2026("dummy_path", case_results)
        mappings = mapper.extra_mappings()

        assert mappings["(option_1)"] is True
        assert mappings["(option_1_all_charges)"] is True
        assert mappings["(option_1_some_charges)"] is False
        assert mappings["(option_2)"] is False
        assert mappings["(option_3)"] is False

    def test_partial_conviction_expungement_selects_option_1_some_charges(self):
        """When some convictions are ineligible, select Option 1 with 'some charges'."""
        charges = [
            make_eligible_conviction("Theft", "case1-1"),
            make_ineligible_conviction("Assault", "case1-2"),
        ]
        case = make_case(charges)
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        mapper = PDFFieldMapper2026("dummy_path", case_results)
        mappings = mapper.extra_mappings()

        assert mappings["(option_1)"] is True
        assert mappings["(option_1_all_charges)"] is False
        assert mappings["(option_1_some_charges)"] is True
        assert mappings["(option_2)"] is False

    def test_dismissals_only_selects_option_2(self):
        """When there are only dismissals (no convictions), select Option 2."""
        charges = [make_eligible_dismissal("Trespass", "case1-1")]
        case = make_case(charges)
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        mapper = PDFFieldMapper2026("dummy_path", case_results)
        mappings = mapper.extra_mappings()

        assert mappings["(option_1)"] is False
        assert mappings["(option_1_all_charges)"] is False
        assert mappings["(option_1_some_charges)"] is False
        assert mappings["(option_2)"] is True

    def test_convictions_and_dismissals_selects_option_1(self):
        """When there are both convictions and dismissals, Option 1 takes precedence."""
        charges = [
            make_eligible_conviction("Theft", "case1-1"),
            make_eligible_dismissal("Trespass", "case1-2"),
        ]
        case = make_case(charges)
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        mapper = PDFFieldMapper2026("dummy_path", case_results)
        mappings = mapper.extra_mappings()

        assert mappings["(option_1)"] is True
        assert mappings["(option_2)"] is False


class TestPDFFieldMapper2026ChargeList:
    """Test that charges are listed correctly for partial expungement."""

    def test_no_charge_list_for_full_conviction_expungement(self):
        """Full conviction expungement should not list individual charges."""
        charges = [make_eligible_conviction("Theft", "case1-1")]
        case = make_case(charges)
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        mapper = PDFFieldMapper2026("dummy_path", case_results)
        mappings = mapper.extra_mappings()

        assert mappings["(charge_name_1)"] == ""
        assert mappings["(charge_count_1)"] == ""

    def test_charge_list_for_partial_expungement_shows_only_convictions(self):
        """Partial expungement should list only eligible convictions, not dismissals."""
        charges = [
            make_eligible_conviction("Theft", "case1-1"),
            make_eligible_dismissal("Trespass", "case1-2"),  # Should NOT be listed
            make_ineligible_conviction("Assault", "case1-3"),
        ]
        case = make_case(charges)
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        mapper = PDFFieldMapper2026("dummy_path", case_results)
        mappings = mapper.extra_mappings()

        # Should only list the eligible conviction, not the dismissal
        assert mappings["(charge_name_1)"] == "Theft"
        assert mappings["(charge_count_1)"] == "1"
        assert mappings["(charge_name_2)"] == ""  # No second charge listed

    def test_no_partial_expungement_when_only_dismissals_ineligible(self):
        """If all convictions are eligible but some dismissals aren't, it's still full expungement."""
        eligible_conviction = make_eligible_conviction("Theft", "case1-1")

        # Make an ineligible dismissal
        ineligible_dismissal = make_eligible_dismissal("Trespass", "case1-2")
        ineligible_dismissal.expungement_result.charge_eligibility.status = ChargeEligibilityStatus.INELIGIBLE

        charges = [eligible_conviction, ineligible_dismissal]
        case = make_case(charges)
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        mapper = PDFFieldMapper2026("dummy_path", case_results)
        mappings = mapper.extra_mappings()

        # Should be full expungement (option_1_all_charges) since all CONVICTIONS are eligible
        assert mappings["(option_1)"] is True
        assert mappings["(option_1_all_charges)"] is True
        assert mappings["(option_1_some_charges)"] is False
        assert mappings["(charge_name_1)"] == ""

    def test_additional_charges_checkbox_when_more_than_5_convictions(self):
        """When there are more than 5 eligible convictions, check additional_charges_attached."""
        charges = [
            make_eligible_conviction(f"Charge{i}", f"case1-{i}") for i in range(1, 7)
        ]
        charges.append(make_ineligible_conviction("Ineligible", "case1-99"))
        case = make_case(charges)
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        mapper = PDFFieldMapper2026("dummy_path", case_results)
        mappings = mapper.extra_mappings()

        assert mappings["(option_1_some_charges)"] is True
        assert mappings["(additional_charges_attached)"] is True
        # Should only fill first 5
        assert mappings["(charge_name_5)"] != ""


class TestPDFFilenameSelection:
    """Test that the correct PDF file is selected."""

    def test_multnomah_uses_old_forms(self):
        """Multnomah county should use the old Multnomah-specific forms."""
        charges = [make_eligible_conviction()]
        case = make_case(charges, county="Multnomah")
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        filename = get_pdf_filename(case_results)
        assert filename == "multnomah_conviction.pdf"

    def test_multnomah_arrest_uses_old_forms(self):
        """Multnomah dismissal should use the old arrest form."""
        charges = [make_eligible_dismissal()]
        case = make_case(charges, county="Multnomah")
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        filename = get_pdf_filename(case_results)
        assert filename == "multnomah_arrest.pdf"

    def test_other_county_conviction_uses_2026_form(self):
        """Non-Multnomah conviction should use the new 2026 conviction form."""
        charges = [make_eligible_conviction()]
        case = make_case(charges, county="Washington")
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        filename = get_pdf_filename(case_results)
        assert filename == "oregon_conviction.pdf"

    def test_other_county_dismissal_uses_2026_form(self):
        """Non-Multnomah dismissal should use the new 2026 arrest form."""
        charges = [make_eligible_dismissal()]
        case = make_case(charges, county="Washington")
        case_results = CaseResults.build(case, USER_DATA, sid="SID123")

        filename = get_pdf_filename(case_results)
        assert filename == "oregon_arrest.pdf"


class TestFormFilling2026CountySelection:
    """Test that the correct form filling method is used per county."""

    def test_should_use_2026_form_for_non_multnomah(self):
        assert FormFilling2026.should_use_2026_form("Washington") is True
        assert FormFilling2026.should_use_2026_form("Lane") is True
        assert FormFilling2026.should_use_2026_form("Baker") is True

    def test_should_not_use_2026_form_for_multnomah(self):
        assert FormFilling2026.should_use_2026_form("Multnomah") is False
        assert FormFilling2026.should_use_2026_form("multnomah") is False
