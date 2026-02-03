"""
Form filling for the 2026 Oregon expungement forms.

This module fills the new January 2026 form (ORS 137.225 or 137.223) while
reusing content computation from form_filling.py.

Key differences from old form:
- Option 1: Court case with conviction - list charges only if partial expungement
- Option 2: Court case with dismissed/acquitted only - no charge list
- Option 3: No court case (N/A for RecordSponge)
"""

from datetime import date
from os import path
from pathlib import Path
from tempfile import mkdtemp
from typing import Any, Dict, List, Optional, Tuple
from zipfile import ZipFile

from expungeservice.form_filling import (
    CaseResults,
    DA_ADDRESSES,
    FormFilling as OldFormFilling,
    PDFFieldMapper,
    PDF,
)
from expungeservice.models.record_summary import RecordSummary


def get_da_address(county: str) -> str:
    """Get the DA address for a county."""
    county_key = county.replace(" ", "_").lower()
    return DA_ADDRESSES.get(county_key, "")


def format_date(d) -> str:
    """Format a date for display on the form."""
    if d is None:
        return ""
    if hasattr(d, 'strftime'):
        return d.strftime("%b %-d, %Y")
    return str(d)


def get_pdf_path(filename: str) -> str:
    """Get the full path to a PDF file in the files directory."""
    source_dir = path.join(Path(__file__).parent, "files")
    return path.join(source_dir, filename)


def get_pdf_filename(case_results: CaseResults) -> str:
    """
    Determine which PDF file to use based on the case.

    Returns the filename (not full path) of the appropriate PDF.
    """
    county = case_results.county.lower()

    # Multnomah has its own forms (unchanged from old system)
    if county == "multnomah":
        return "multnomah_conviction.pdf" if case_results.has_conviction else "multnomah_arrest.pdf"

    # All other counties use new 2026 forms
    if case_results.has_conviction:
        return "oregon_conviction.pdf"
    else:
        return "oregon_arrest.pdf"


def get_sorted_eligible_charges(case_results: CaseResults) -> List:
    """Get eligible charges sorted by count number."""
    eligible_charges = case_results.eligible_charges_list

    def get_count_num(charge):
        if charge.ambiguous_charge_id:
            try:
                return int(charge.ambiguous_charge_id.split("-")[-1])
            except ValueError:
                return 999
        return 999

    return sorted(eligible_charges, key=get_count_num)


class PDFFieldMapper2026(PDFFieldMapper):
    """
    Field mapper for the 2026 Oregon expungement form.

    This maps the new form's field names to values computed from CaseResults.
    """

    def extra_mappings(self):
        s = self.source_data
        if not isinstance(s, CaseResults):
            # OSP Form - delegate to parent
            return super().extra_mappings()

        today = date.today().strftime("%b %-d, %Y")

        # Determine which option applies
        # Option 1: Has conviction (including contempt/GEI)
        # Option 2: Dismissed/acquitted only
        # Option 3: No court case (N/A for RecordSponge)
        is_option_1 = s.has_conviction
        is_option_2 = s.has_dismissed and not s.has_conviction

        # For Option 1, partial expungement only if there are ineligible CONVICTIONS
        # (not just any ineligible charges - dismissed charges don't matter here)
        ineligible_convictions = [c for c in s.ineligible_charges._charges if c.convicted()]
        has_ineligible_convictions = len(ineligible_convictions) > 0
        is_partial_expungement = is_option_1 and has_ineligible_convictions

        # Get first arrest date
        arrest_dates = s.arrest_dates
        first_arrest_date = format_date(arrest_dates[0]) if arrest_dates else ""

        # Build the mapping
        mapping = {
            # Header fields
            "(county)": s.county,
            "(case_number)": s.case_number_with_comments if is_partial_expungement else s.case_number,
            "(defendant_name)": s.case_name,
            "(dob)": s.date_of_birth,
            "(sid_number)": s.sid or "",
            "(law_enforcement_agency)": "Not Known",  # Per guidance, to avoid rejection
            "(arrest_date)": first_arrest_date,
            "(fpn_number)": "",  # Leave blank

            # Option checkboxes
            "(option_1)": is_option_1,
            "(option_1_all_charges)": is_option_1 and not is_partial_expungement,
            "(option_1_some_charges)": is_partial_expungement,
            "(option_2)": is_option_2,
            "(option_3)": False,  # N/A for RecordSponge

            # Additional charges checkbox
            "(additional_charges_attached)": False,

            # Declaration checkboxes (page 2) - always true for eligible cases
            "(waited_required_period)": True,
            "(legally_eligible)": True,
            "(filed_fingerprints)": True,
            "(will_serve_copy)": True,

            # Option 1 additional checkboxes (only if has conviction)
            "(not_currently_charged)": is_option_1,
            "(paid_osp_fee)": is_option_1,
            "(complied_sentence)": is_option_1,

            # Additional offenses checkbox
            "(additional_offenses_attached)": False,

            # Signature section
            "(declaration_date)": today,
            "(signature)": "",  # User signs
            "(email)": s.email_address,
            "(printed_name)": s.full_name,
            "(address)": s.mailing_address,
            "(city_state_zip)": f"{s.city}, {s.state} {s.zip_code}",
            "(phone)": s.phone_number,

            # Certificate of mailing
            "(mailing_date)": today,
            "(prosecutor_address)": get_da_address(s.county),
            "(certificate_date)": today,
            "(defendant_signature_certificate)": "",  # User signs
            "(defendant_name_printed)": s.full_name,

            # Track for warnings
            "(has_ineligible_charges)": s.has_ineligible_charges,
        }

        # Initialize all charge fields to empty
        for i in range(1, 6):
            mapping[f"(charge_name_{i})"] = ""
            mapping[f"(charge_count_{i})"] = ""

        # Fill charge names only for partial expungement (Option 1 with some ineligible convictions)
        # List ALL eligible charges (convictions AND dismissals), sorted by count number
        if is_partial_expungement:
            sorted_charges = get_sorted_eligible_charges(s)

            for i, charge in enumerate(sorted_charges[:5]):  # Max 5 charges in table
                mapping[f"(charge_name_{i+1})"] = charge.name.title()
                # Get the count number from charge ID (last part after hyphen)
                count_num = charge.ambiguous_charge_id.split("-")[-1] if charge.ambiguous_charge_id else str(i+1)
                mapping[f"(charge_count_{i+1})"] = count_num

            if len(sorted_charges) > 5:
                mapping["(additional_charges_attached)"] = True

        # Offense fields (for Option 3 - not used in RecordSponge)
        for i in range(1, 6):
            mapping[f"(offense_{i})"] = ""

        return mapping


def build_appendix_text(extra_charges: List) -> str:
    """Build markdown text for the appendix listing additional charges."""
    lines = ["# Additional Eligible Charges to Be Set Aside", ""]
    lines.append("| Count | Charge Name |")
    lines.append("|-------|-------------|")

    for charge in extra_charges:
        count_num = charge.ambiguous_charge_id.split("-")[-1] if charge.ambiguous_charge_id else "?"
        charge_name = charge.name.title()
        lines.append(f"| {count_num} | {charge_name} |")

    return "\n".join(lines)


def create_filled_pdf(case_results: CaseResults, user_info: Dict[str, str]) -> Tuple[Optional[PDF], Optional[str]]:
    """
    Create a filled PDF for a case using the 2026 form.

    Returns a tuple of (pdf, suggested_filename), or (None, None) for Multnomah.
    """
    pdf_filename = get_pdf_filename(case_results)
    pdf_path = get_pdf_path(pdf_filename)

    # Check if this is a Multnomah case (use old form filling)
    if case_results.county.lower() == "multnomah":
        # Fall back to old form filling for Multnomah
        return None, None

    # Create case results with user info
    # CaseResults already has the user info from build()
    mapper = PDFFieldMapper2026(pdf_path, case_results)
    pdf = PDF.fill_form(mapper)

    # Check if we need an appendix for extra charges (partial expungement with >5 eligible)
    ineligible_convictions = [c for c in case_results.ineligible_charges._charges if c.convicted()]
    is_partial_expungement = case_results.has_conviction and len(ineligible_convictions) > 0

    if is_partial_expungement:
        sorted_charges = get_sorted_eligible_charges(case_results)
        if len(sorted_charges) > 5:
            extra_charges = sorted_charges[5:]
            appendix_text = build_appendix_text(extra_charges)
            pdf.add_text_at_end(appendix_text)

    # Build filename
    base_name = case_results.county.lower()
    if case_results.has_conviction:
        base_name += "_conviction"
    else:
        base_name += "_arrest"

    suggested_filename = f"{case_results.case_name}_{case_results.case_number}_{base_name}.pdf"

    return pdf, suggested_filename


class FormFilling2026:
    """
    Main class for building expungement packets with the 2026 forms.
    """

    # Counties that still use old forms
    NON_2026_COUNTIES = ["multnomah"]

    @staticmethod
    def should_use_2026_form(county: str) -> bool:
        """Check if a county should use the 2026 form."""
        return county.lower() not in FormFilling2026.NON_2026_COUNTIES

    @staticmethod
    def build_zip(
        record_summary: RecordSummary,
        user_information_dict: Dict[str, str],
        summary_pdf_bytes: bytes,
        summary_filename: str
    ) -> Tuple[str, str]:
        """
        Build a zip file containing all expungement forms.

        This is the main entry point, replacing FormFilling.build_zip().
        """
        temp_dir = mkdtemp()
        zip_file_name = "expungement_packet.zip"
        zip_path = path.join(mkdtemp(), zip_file_name)
        zip_file = ZipFile(zip_path, "w")

        sid = FormFilling2026._unify_sids(record_summary)

        all_case_results = []
        all_motions_to_set_aside = []
        has_eligible_convictions = False

        for case in record_summary.record.cases:
            case_results = CaseResults.build(case, user_information_dict, sid)

            if case_results.get_has_eligible_convictions:
                has_eligible_convictions = True

            all_case_results.append(case_results)

            if case_results.is_expungeable_now:
                # Determine which form filling to use
                if FormFilling2026.should_use_2026_form(case_results.county):
                    # Use new 2026 form filling
                    pdf, filename = create_filled_pdf(case_results, user_information_dict)
                    if pdf and filename:
                        file_path = path.join(temp_dir, filename)
                        pdf.write(file_path)
                        zip_file.write(file_path, filename)
                        all_motions_to_set_aside.append((file_path, filename))
                else:
                    # Use old form filling for Multnomah
                    file_info = OldFormFilling._create_and_write_pdf(case_results, temp_dir)
                    zip_file.write(*file_info[0:2])
                    all_motions_to_set_aside.append(file_info[0:2])

        # Create OSP form (use old logic)
        user_info_for_osp: Dict[str, Any] = {**user_information_dict}
        user_info_for_osp["counties_with_cases_to_expunge"] = FormFilling2026._counties_with_cases_to_expunge(
            all_case_results
        )
        user_info_for_osp["has_eligible_convictions"] = has_eligible_convictions
        osp_file_info = OldFormFilling._create_and_write_pdf(user_info_for_osp, temp_dir)
        zip_file.write(*osp_file_info[0:2])

        # Build compiled PDF
        if all_motions_to_set_aside:
            file_paths = [f[0] for f in all_motions_to_set_aside] + [osp_file_info[0]]
            comp_name = "COMPILED.pdf"
            comp_path = path.join(temp_dir, comp_name)
            OldFormFilling.compile_pdfs(file_paths, comp_path)
            zip_file.write(comp_path, comp_name)

        # Add summary PDF
        summary_path = path.join(temp_dir, summary_filename)
        with open(summary_path, 'wb') as summary_file:
            summary_file.write(summary_pdf_bytes)
        zip_file.write(summary_path, summary_filename)

        zip_file.close()

        return zip_path, zip_file_name

    @staticmethod
    def _unify_sids(record_summary: RecordSummary) -> str:
        """Get the first non-empty SID from the record."""
        for case in record_summary.record.cases:
            if case.summary.sid:
                return case.summary.sid
        return ""

    @staticmethod
    def _counties_with_cases_to_expunge(all_case_results: List[CaseResults]) -> List[str]:
        """Get list of counties with eligible charges."""
        counties: List[str] = []
        for case_result in all_case_results:
            if (
                case_result.has_eligible_charges and
                case_result.case.summary.balance_due_in_cents == 0 and
                case_result.case.summary.location not in counties
            ):
                counties.append(case_result.case.summary.location)
        return counties
