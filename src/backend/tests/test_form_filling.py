import os
from tempfile import mkdtemp
from zipfile import ZipFile
from os import path
from pathlib import Path

import pytest
from pdfrw import PdfReader

from expungeservice.expunger import Expunger
from expungeservice.form_filling import FormFilling, AcroFormMapper as AFM
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
def get_pdf_dict(pdf: PdfReader):
    return {field.T: field.V for field in pdf.Root.AcroForm.Fields}

def assert_pdf_values(pdf: PdfReader, expected):
    pdf_dict = get_pdf_dict(pdf)

    for (key, value) in expected.items():
        assert pdf_dict[key] == value
        
def assert_other_fields_not_checked(pdf, checked_fields):
    pdf_dict = get_pdf_dict(pdf)
    constant_fields = TestOregon022023AcroFormMapper.constant_fields.keys()

    for (key, value) in pdf_dict.items():
        if not checked_fields.get(key) and key not in constant_fields:
            assert value != "X"

class TestOregon022023AcroFormMapper:
    constant_fields = {
        "(Plaintiff)": "State of Oregon",
        "(I am not currently charged with a crime)": "X",
        "(The arrest or citation I want to set aside is not for a charge of Driving Under the Influence of)": "X",
        "(have sent)": "X"
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
        "(Signature_2)": None
    }
    form_data_string_fields = {
        "(FOR THE COUNTY OF)": "county_ACTUAL",
        "(Case No)": "case_number_ACTUAL",
        "(Defendant)": "case_name_ACTUAL",
        "(DOB)": "date_of_birth_ACTUAL",
        "(SID)": "sid_ACTUAL",
        "(Date of conviction contempt finding or judgment of GEI)": "conviction_dates_ACTUAL",
        "(Date of arrest)": "dismissed_arrest_dates_ACTUAL",
        "(Arresting Agency)": "arresting_agency_ACTUAL",
        "(Name typed or printed)": "full_name_ACTUAL",
        "(Address)": "address_ACTUAL,  city_ACTUAL,  state_ACTUAL,  zip_code_ACTUAL,  phone_number_ACTUAL",
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
    def pdf(self):
        file_path = path.join(
            Path(__file__).parent.parent, "expungeservice", "files", "oregon.pdf"
        )
        return PdfReader(file_path)

    def test_key_is_mapped_to_a_function_returns_the_function_value(self):
        mapper = AFM( {"Plaintiff": "NOT SEEN"})
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

    def test_all_the_fields_are_accounted_for(self, pdf):
        AFM.update_pdf_fields(pdf, opts={"assert_blank_pdf": True})
        field_types = [
            "ignored_fields", "constant_fields", "form_data_string_fields",
            "form_data_boolean_fields"
        ]

        assert len(pdf.Root.AcroForm.Fields) == sum(
            len(getattr(self, type)) for type in field_types
        )

    def test_pdf_string_values_from_form_data(self, pdf):
        form_data = {
            "county": "county_ACTUAL",
            "case_number": "case_number_ACTUAL",
            "case_name": "case_name_ACTUAL",
            "date_of_birth": "date_of_birth_ACTUAL",
            "sid": "sid_ACTUAL",
            "conviction_dates": "conviction_dates_ACTUAL",
            "dismissed_arrest_dates": "dismissed_arrest_dates_ACTUAL",
            "arresting_agency": "arresting_agency_ACTUAL",
            "full_name": "full_name_ACTUAL",
            "mailing_address": "address_ACTUAL",
            "city": "city_ACTUAL",
            "state": "state_ACTUAL",
            "zip_code": "zip_code_ACTUAL",
            "phone_number": "phone_number_ACTUAL",
            "da_address": "da_address_ACTUAL",
            "full_name": "full_name_ACTUAL",
        }

        AFM.update_pdf_fields(pdf, form_data, opts={"assert_blank_pdf": True})
        assert_pdf_values(pdf, self.form_data_string_fields)

    def test_pdf_values_that_are_ignored_and_constant(self, pdf):
        mapper = AFM.update_pdf_fields(pdf, opts={"assert_blank_pdf": True})
        assert len(mapper.ignored_keys) == len(self.ignored_fields)

        for name in self.ignored_fields.keys() :
            assert mapper.ignored_keys[name] is None

        assert_pdf_values(pdf, self.constant_fields)

    # boolean field tests
    def test_pdf_boolean_has_no_complaint_fields_are_updated(self, pdf):
        form_data = {"has_no_complaint": "X"}
        expected_fields = {
            "(record of arrest with no charges filed)": "X",
            "(no accusatory instrument was filed and at least 60 days have passed since the)": "X"
        }
        AFM.update_pdf_fields(pdf, form_data, opts={"assert_blank_pdf": True})
        assert_pdf_values(pdf, expected_fields)
        assert_other_fields_not_checked(pdf, expected_fields)

        new_form_data = {"has_no_complaint": ""}
        new_expected_fields = {
            "(record of arrest with charges filed and the associated check all that apply)": "X",
        }
        AFM.update_pdf_fields(pdf, new_form_data)
        assert_pdf_values(pdf, new_expected_fields)
        assert_other_fields_not_checked(pdf, new_expected_fields)

    def test_pdf_boolean_has_conviction_fields_are_updated(self, pdf):
        form_data = {"has_conviction": "X"}
        expected_fields = {
            "(conviction)": "X",
            "(ORS 137225 does not prohibit a setaside of this conviction see Instructions)": "X",
            "(I have fully completed complied with or performed all terms of the sentence of the court)": "X"
        }
        AFM.update_pdf_fields(pdf, form_data, opts={"assert_blank_pdf": True})
        assert_pdf_values(pdf, expected_fields)
        assert_other_fields_not_checked(pdf, expected_fields)

# TODO finish testing boolean fields
