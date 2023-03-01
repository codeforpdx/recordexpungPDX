import os
from tempfile import mkdtemp
from zipfile import ZipFile
from typing import List, Dict
import re

import pytest

from expungeservice.expunger import Expunger
from expungeservice.form_filling import FormFilling, PDF, AcroFormMapper as AFM
from expungeservice.record_merger import RecordMerger
from expungeservice.record_summarizer import RecordSummarizer
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe


def test_normal_conviction_uses_multnomah_conviction_form():
    record = CrawlerFactory.create(JohnDoe.SINGLE_CASE_RECORD, {"CASEJD1": CaseDetails.CASEJD74})
    expunger_result = Expunger.run(record)
    merged_record = RecordMerger.merge([record], [expunger_result], [])
    record_summary = RecordSummarizer.summarize(merged_record, {})
    user_information = {
        "full_name": "",
        "date_of_birth": "",
        "mailing_address": "",
        "phone_number": "",
        "city": "",
        "state": "",
        "zip_code": "",
    }
    zip_path, zip_name = FormFilling.build_zip(record_summary, user_information)
    temp_dir = mkdtemp()
    with ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)
        for _root, _dir, files in os.walk(temp_dir):
            assert len(files) == 1


#########################################


class TestOregon022023AcroFormMapper:
    def test_key_is_mapped_to_a_function_returns_the_function_value(self):
        mapper = AFM({"Plaintiff": "NOT SEEN"})
        assert mapper.get("(Plaintiff)") == "State of Oregon"

    def test_key_exists_and_has_a_value_in_form_data(self):
        mapper = AFM({"county": "baker"})
        assert mapper.get("(FOR THE COUNTY OF)") == "baker"

    def test_key_exists_but_its_value_does_not(self):
        mapper = AFM({"DOB": None})
        assert mapper.get("(DOB)") == ""

    def test_an_undefined_key_returns_empty_string(self):
        mapper = AFM({"only in form data": "foo"})
        assert mapper.get("only in form data") == ""


#########################################


def assert_pdf_values(pdf: PDF, expected: Dict[str, str]):
    annotation_dict = pdf.get_annotation_dict()
    for key, value in annotation_dict.items():
        annotation_dict[key] = re.sub(r"\(|\)", "", value) if value else None

    for key, value in expected.items():
        assert annotation_dict[key] == value, f"key: {key}"


def assert_other_fields_not_checked(pdf: PDF, checked_fields):
    annotation_dict = pdf.get_annotation_dict()
    constant_fields = TestOregonPDF.constant_fields.keys()

    for key, value in annotation_dict.items():
        if not checked_fields.get(key) and key not in constant_fields:
            assert value != "/On", key


def assert_pdf_boolean_field(pdf: PDF, field_name: str, expected_field_names: List[str]):
    form_data = {field_name: FormFilling.CHECK_MARK}
    expected_fields = {field_name: "/On" for field_name in expected_field_names}

    pdf.update_annotations(form_data, opts={"assert_blank_pdf": True})
    assert_pdf_values(pdf, expected_fields)
    assert_other_fields_not_checked(pdf, expected_fields)


class TestOregonPDF:
    constant_fields = {
        "(Plaintiff)": "State of Oregon",
        "(I am not currently charged with a crime)": "/On",
        "(The arrest or citation I want to set aside is not for a charge of Driving Under the Influence of)": "/On",
        "(have sent)": "/On",
    }
    ignored_fields = {
        "(Fingerprint number FPN  if known)": None,
        "(finding of Guilty Except for Insanity GEI)": None,
        "(provided in ORS 137223)": None,
        "(PSRB)": None,
        "(My probation WAS NOT revoked)": None,
        "(If no arrest date date of citation booking or incident)": None,
        "(will send a copy of my fingerprints to the Department of State Police)": None,
        "(Date)": None,
        "(Signature)": None,
        "(States mail a true and complete copy of this Motion to Set Aside and Declaration in Support to)": None,
        "(delivered or)": None,
        "(placed in the United)": None,
        "(the District Attorney at address 1)": None,
        "(the District Attorney at address 3)": None,
        "(Date_2)": None,
        "(Signature_2)": None,
    }
    form_data_string_fields = {
        "(FOR THE COUNTY OF)": "county_ACTUAL",
        "(Case No)": "case_number_ACTUAL",
        "(Defendant)": "case_name_ACTUAL",
        "(DOB)": "date_of_birth_ACTUAL",
        "(SID)": "sid_ACTUAL",
        "(Date of conviction contempt finding or judgment of GEI)": "conviction_dates_ACTUAL",
        "(Date of arrest)": "arrest_dates_all_ACTUAL",
        "(Arresting Agency)": "arresting_agency_ACTUAL",
        "(Name typed or printed)": "full_name_ACTUAL",
        "(Address)": "address_ACTUAL,    city_ACTUAL,    state_ACTUAL,    zip_code_ACTUAL,    phone_number_ACTUAL",
        "(the District Attorney at address 2)": "da_address_ACTUAL",
        "(Name typed or printed_2)": "full_name_ACTUAL",
    }
    form_data_boolean_fields = {
        "(record of arrest with no charges filed)": "has_no_complaint",
        "(record of arrest with charges filed and the associated check all that apply)": "!has_no_complaint",
        "(conviction)": "has_conviction",
        "(record of citation or charge that was dismissedacquitted)": "has_dismissed",
        "(contempt of court finding)": "has_contempt_of_court",
        "(ORS 137225 does not prohibit a setaside of this conviction see Instructions)": "has_conviction",
        "(Felony  Class B and)": "has_class_b_felony",
        "(Felony  Class C and)": "has_class_c_felony",
        "(Misdemeanor  Class A and)": "has_class_a_misdemeanor",
        "(Misdemeanor  Class B or C and)": "has_class_bc_misdemeanor",
        "(Violation or Contempt of Court and)": "has_violation_or_contempt_of_court",
        "(7 years have passed since the later of the convictionjudgment or release date and)": "has_class_b_felony",
        "(I have not been convicted of any other offense or found guilty except for insanity in)": "has_class_b_felony",
        "(5 years have passed since the later of the convictionjudgment or release date and)": "has_class_c_felony",
        "(I have not been convicted of any other offense or found guilty except for insanity in_2)": "has_class_c_felony",
        "(3 years have passed since the later of the convictionjudgment or release date and)": "has_class_a_misdemeanor",
        "(I have not been convicted of any other offense or found guilty except for insanity in_3)": "has_class_a_misdemeanor",
        "(1 year has passed since the later of the convictionfindingjudgment or release)": "has_class_bc_misdemeanor",
        "(I have not been convicted of any other offense or found guilty except for insanity)": "has_class_bc_misdemeanor",
        "(1 year has passed since the later of the convictionfindingjudgment or release_2)": "has_violation_or_contempt_of_court",
        "(I have not been convicted of any other offense or found guilty except for insanity_2)": "has_violation_or_contempt_of_court",
        "(I have fully completed complied with or performed all terms of the sentence of the court)": "has_conviction",
        "(I was sentenced to probation in this case and)": "has_probation_revoked",
        "(My probation WAS revoked and 3 years have passed since the date of revocation)": "has_probation_revoked",
        "(no accusatory instrument was filed and at least 60 days have passed since the)": "has_no_complaint",
        "(an accusatory instrument was filed and I was acquitted or the case was dismissed)": "has_dismissed",
    }

    @pytest.fixture
    def pdf(self) -> PDF:
        return PDF("oregon", {"assert_blank_pdf": True})

    def test_all_the_fields_are_accounted_for(self, pdf: PDF):
        field_types = ["ignored_fields", "constant_fields", "form_data_string_fields", "form_data_boolean_fields"]
        grouped_field_names = [(getattr(self, type).keys()) for type in field_types]
        field_names = set(field_name for subgroup in grouped_field_names for field_name in subgroup)

        assert set(pdf.get_field_dict().keys()) == field_names
        assert set(anot.T for anot in pdf.annotations) == field_names

    def test_pdf_string_values_from_form_data(self, pdf: PDF):
        form_data = {
            "county": "county_ACTUAL",
            "case_number": "case_number_ACTUAL",
            "case_name": "case_name_ACTUAL",
            "date_of_birth": "date_of_birth_ACTUAL",
            "sid": "sid_ACTUAL",
            "conviction_dates": "conviction_dates_ACTUAL",
            "arrest_dates_all": "arrest_dates_all_ACTUAL",
            "dismissed_arrest_dates": "dismissed_arrest_dates_ACTUAL",
            "arresting_agency": "arresting_agency_ACTUAL",
            "full_name": "full_name_ACTUAL",
            "mailing_address": "address_ACTUAL",
            "city": "city_ACTUAL",
            "state": "state_ACTUAL",
            "zip_code": "zip_code_ACTUAL",
            "phone_number": "phone_number_ACTUAL",
            "da_address": "da_address_ACTUAL",
        }

        pdf.update_annotations(form_data)
        assert_pdf_values(pdf, self.form_data_string_fields)

    def test_pdf_values_that_are_ignored_or_constant(self, pdf: PDF):
        mapper = pdf.update_annotations()
        ignored_field_names = (field_name for field_name in self.ignored_fields.keys())

        assert set(mapper.ignored_keys) == set(ignored_field_names)
        assert_pdf_values(pdf, self.constant_fields)

    def test_pdf_boolean_has_no_complaint_on(self, pdf: PDF):
        assert_pdf_boolean_field(
            pdf,
            "has_no_complaint",
            [
                "(record of arrest with no charges filed)",
                "(no accusatory instrument was filed and at least 60 days have passed since the)",
            ],
        )

    def test_pdf_boolean_has_no_complaint_off(self, pdf: PDF):
        form_data = {"has_no_complaint": ""}
        expected_fields = {
            "(record of arrest with charges filed and the associated check all that apply)": "/On",
        }
        pdf.update_annotations(form_data)
        assert_pdf_values(pdf, expected_fields)
        assert_other_fields_not_checked(pdf, expected_fields)

    def test_pdf_boolean_has_conviction(self, pdf: PDF):
        assert_pdf_boolean_field(
            pdf,
            "has_conviction",
            [
                "(conviction)",
                "(ORS 137225 does not prohibit a setaside of this conviction see Instructions)",
                "(I have fully completed complied with or performed all terms of the sentence of the court)",
            ],
        )

    def test_pdf_boolean_has_dismissed(self, pdf: PDF):
        assert_pdf_boolean_field(
            pdf,
            "has_dismissed",
            [
                "(record of citation or charge that was dismissedacquitted)",
                "(an accusatory instrument was filed and I was acquitted or the case was dismissed)",
            ],
        )

    def test_pdf_boolean_has_contempt_of_court(self, pdf: PDF):
        assert_pdf_boolean_field(pdf, "has_contempt_of_court", ["(contempt of court finding)"])

    def test_pdf_boolean_has_class_b_felony(self, pdf: PDF):
        assert_pdf_boolean_field(
            pdf,
            "has_class_b_felony",
            [
                "(Felony  Class B and)",
                "(7 years have passed since the later of the convictionjudgment or release date and)",
                "(I have not been convicted of any other offense or found guilty except for insanity in)",
            ],
        )

    def test_pdf_boolean_has_class_c_felony(self, pdf: PDF):
        assert_pdf_boolean_field(
            pdf,
            "has_class_c_felony",
            [
                "(Felony  Class C and)",
                "(5 years have passed since the later of the convictionjudgment or release date and)",
                "(I have not been convicted of any other offense or found guilty except for insanity in_2)",
            ],
        )

    def test_pdf_boolean_has_class_a_misdemeanor(self, pdf: PDF):
        assert_pdf_boolean_field(
            pdf,
            "has_class_a_misdemeanor",
            [
                "(Misdemeanor  Class A and)",
                "(3 years have passed since the later of the convictionjudgment or release date and)",
                "(I have not been convicted of any other offense or found guilty except for insanity in_3)",
            ],
        )

    def test_pdf_boolean_has_class_bc_misdemeanor(self, pdf: PDF):
        assert_pdf_boolean_field(
            pdf,
            "has_class_bc_misdemeanor",
            [
                "(Misdemeanor  Class B or C and)",
                "(1 year has passed since the later of the convictionfindingjudgment or release)",
                "(I have not been convicted of any other offense or found guilty except for insanity)",
            ],
        )

    def test_pdf_boolean_has_violation_or_contempt_of_court(self, pdf: PDF):
        assert_pdf_boolean_field(
            pdf,
            "has_violation_or_contempt_of_court",
            [
                "(Violation or Contempt of Court and)",
                "(1 year has passed since the later of the convictionfindingjudgment or release_2)",
                "(I have not been convicted of any other offense or found guilty except for insanity_2)",
            ],
        )

    def test_pdf_boolean_has_probation_revoked(self, pdf: PDF):
        assert_pdf_boolean_field(
            pdf,
            "has_probation_revoked",
            [
                "(I was sentenced to probation in this case and)",
                "(My probation WAS revoked and 3 years have passed since the date of revocation)",
            ],
        )

    # TODO some fields seem to need a different calculation
    # def test_font_is_decreased_as_needed(self, pdf: PDF):
    #     form_data = {"date_of_birth": "123456789a1234567"}
    #     pdf.update_annotations(form_data, {"assert_blank_pdf": True});
    #     font_string = [annotation.DA for annotation in pdf.annotations if annotation.T == '(DOB)'][0]

    #     pdf.write('foo_test')
    #     assert font_string == "(/TimesNewRoman 6 Tf 0 g)"
    #     assert len(pdf.warnings) == 1
    #     assert pdf.warnings[0] == "The font size of \"123456789a123456\" was shrunk to fit the bounding box of \"DOB\". An addendum might be required if it still doesn't fit."


class TestOregonWithConvictionOrderPDF:
    def test_both_old_and_new_fields_are_updated(self):
        pdf = PDF("oregon_with_conviction_order", {"assert_blank_pdf": True})
        form_data = {
            # new form fields
            "sid": "new sid",
            "has_no_complaint": FormFilling.CHECK_MARK,
            # old form fields
            "county": "old county",
            "case_number": "old number",
            "case_name": "old case_name",
            "arrest_dates_all": "old arrest_dates_all",
            "charges_all": "old charges_all",
            "arresting_agency": "old arresting_agency",
            "conviction_dates": "old conviction_dates",
            "conviction_charges": "old conviction_charges",
        }
        expected_pdf_fields = {
            "(SID)": "new sid",
            "(record of arrest with no charges filed)": "/On",
            "(no accusatory instrument was filed and at least 60 days have passed since the)": "/On",
            "(County)": "old county",
            "(Case Number)": "old number",
            "(Case Name)": "old case_name",
            "(Arrest Dates All)": "old arrest_dates_all",
            "(Charges All)": "old charges_all",
            "(Conviction Dates)": "old conviction_dates",
            "(Conviction Charges)": "old conviction_charges",
        }

        pdf.update_annotations(form_data, opts={"assert_blank_pdf": True})
        assert_pdf_values(pdf, expected_pdf_fields)


class TestOregonWithArrestOrderPDF:
    def test_both_old_and_new_fields_are_updated(self):
        pdf = PDF("oregon_with_arrest_order", {"assert_blank_pdf": True})
        form_data = {
            # new form fields
            "sid": "new sid",
            "has_no_complaint": FormFilling.CHECK_MARK,
            # old form fields
            "county": "old county",
            "case_number": "old number",
            "case_name": "old case_name",
            "dismissed_arrest_dates": "old dismissed_arrest_dates",
            "dismissed_charges": "old dismissed_charges",
            "arresting_agency": "old arresting_agency",
            "dismissed_dates": "old dismissed_dates",
        }
        expected_pdf_fields = {
            "(SID)": "new sid",
            "(record of arrest with no charges filed)": "/On",
            "(no accusatory instrument was filed and at least 60 days have passed since the)": "/On",
            "(County)": "old county",
            "(Case Number)": "old number",
            "(Case Name)": "old case_name",
            "(Dismissed Arrest Dates)": "old dismissed_arrest_dates",
            "(Dismissed Charges)": "old dismissed_charges",
            "(Dismissed Dates)": "old dismissed_dates",
        }

        pdf.update_annotations(form_data, opts={"assert_blank_pdf": True})
        assert_pdf_values(pdf, expected_pdf_fields)
        # Validate downloaded PDF in Chrome, Firefox, Safari, Acrobat Reader and Preview
        # pdf.write('foo_test')
