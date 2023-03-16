from datetime import datetime
from typing import Dict, List, Tuple


class MarkdownSerializer:
    @staticmethod
    def to_markdown(record: Dict, header: str) -> str:
        open_cases_block = MarkdownSerializer._gen_open_cases_block(record)
        disclaimer = MarkdownSerializer.disclaimer_and_assumptions(open_cases_block)
        eligible_charges_block = MarkdownSerializer._gen_eligible_charges_block(record)
        eligible_charges_if_balance_paid_block = MarkdownSerializer._gen_eligible_charges_if_balance_paid_block(record)
        ineligible_charges_block = MarkdownSerializer._gen_ineligible_charges_block(record)
        future_eligible_block = MarkdownSerializer._gen_future_eligible_block(record)
        needs_more_analysis_block = MarkdownSerializer._gen_needs_more_analysis_block(record)
        return f"{header}  \n{disclaimer}  \n{eligible_charges_block}  \n{ineligible_charges_block}  \n{eligible_charges_if_balance_paid_block} \n{future_eligible_block}  \n{needs_more_analysis_block}"

    @staticmethod
    def disclaimer_and_assumptions(open_cases_block):
        return f"""## PLEASE READ THIS 

### Disclaimer:
RecordSponge is not your lawyer. The results below should be used as a guide only. If you are relying on this information to expunge your record, please email roe@qiu-qiulaw.com for free consultation.  \n

{open_cases_block}

### Assumptions
<b>1) Successful completion of court requirements</b> &nbsp; If you are currently on probation or conditional discharge, the analysis below assumes that you will successfully complete those requirements.  \n
<b>2) Court debt paid off</b> &nbsp; You must pay off all court debt on a case before you file for expungement on any case which you are otherwise eligible to expunge.  \n
<b>3) No records outside of Oregon State court from last seven years</b> &nbsp; We are only able to access your public Oregon records. Your analysis may be different if you have had cases from <b>within the last seven years</b> which were:  \n
  * from States besides Oregon
  * from Federal Court (in any State)
  * from local District Courts, e.g. Medford Municipal Court (not Jackson Circuit Court)
  * already expunged 

Below is a summary of your eligibility for expungement based on the assumptions above. 
If the above assumptions are not true for you and you would like an updated analysis, email roe@qiu-qiulaw.com with your name and date of birth with subject line, “Updated Analysis”."""

    @staticmethod
    def default_header(aliases):
        header = f"# EXPUNGEMENT ANALYSIS REPORT  \n## Search Terms  \n"
        for alias in aliases:
            name = f"{alias.get('first_name', '')} {alias.get('middle_name','')} {alias.get('last_name','')}".upper()
            name_line = f"Name: {name} " if name else ""
            dob = f"DOB: {alias.get('birth_date')}  \n" if alias.get("birth_date") else " \n"
            alias_line = name_line + dob
            header += alias_line
        return header

    @staticmethod
    def _gen_open_cases_block(record):
        has_open_cases = ["open case" in error for error in record["errors"]]
        if has_open_cases:
            return """<b>You have open charges. You are not eligible to expunge ANY records, including old charges, while you have open charges.</b>"""
        else:
            return ""

    @staticmethod
    def _build_listed_charges(eligible_case_charges_tuples: List[Tuple[str, List[Tuple[str, str]]]]) -> str:
        listed_charges = ""
        print("build...", eligible_case_charges_tuples)
        for case_info, charges_info in eligible_case_charges_tuples:
            if case_info:
                listed_charges += f" - {case_info} \n"
                charges = [description for id, description in charges_info]
                listed_charges += "     - " + " \n     - ".join(charges) + " \n"
            else:
                charges = [description for id, description in charges_info]
                listed_charges += " - " + " \n - ".join(charges) + " \n"
        return listed_charges

    @staticmethod
    def _gen_eligible_charges_block(record):
        eligible_case_charges_tuples = [
            x for x in record["summary"]["charges_grouped_by_eligibility_and_case"] if x[0] == "Eligible Now"
        ]
        if len(eligible_case_charges_tuples) > 0:
            listed_charges = MarkdownSerializer._build_listed_charges(eligible_case_charges_tuples[0][1])
        else:
            listed_charges = "You are not currently eligible to expunge any charges."
        return "## Charges Eligible Now  \n" + listed_charges + "  \n"

    @staticmethod
    def _gen_eligible_charges_if_balance_paid_block(record):
        eligible_case_charges_tuples = [
            x
            for x in record["summary"]["charges_grouped_by_eligibility_and_case"]
            if x[0] == "Eligible Now If Balance Paid"
        ]

        if len(eligible_case_charges_tuples) > 0:
            listed_charges = MarkdownSerializer._build_listed_charges(eligible_case_charges_tuples[0][1])
            return f"## Charges Eligible Now If Balance Paid  \nThese convictions are eligible as soon as the balance of fines on the case is paid.  \n\n{listed_charges}  \n"
        else:
            return ""

    @staticmethod
    def _gen_ineligible_charges_block(record):
        ineligible_case_charges_tuples = [
            x for x in record["summary"]["charges_grouped_by_eligibility_and_case"] if x[0] == "Ineligible"
        ]
        if len(ineligible_case_charges_tuples) > 0:
            listed_charges = MarkdownSerializer._build_listed_charges(ineligible_case_charges_tuples[0][1])
            return f"## Ineligible Charges  \nThese convictions are not eligible for expungement at any time under the current law.  \n\n{listed_charges}  \n"
        else:
            return ""

    @staticmethod
    def _gen_future_eligible_block(record):
        eligible_charges_by_date = record["summary"]["charges_grouped_by_eligibility_and_case"]
        future_eligible_charges = [
            (key, eligible_charges_for_date)
            for key, eligible_charges_for_date in eligible_charges_by_date
            if key not in ["Eligible Now", "Ineligible", "Needs More Analysis", "Eligible Now If Balance Paid"]
        ]
        if future_eligible_charges:
            text_block = "## Future Eligible Charges  \nThe following charges (dismissed and convicted) are eligible at the designated dates. Convictions in the future will set your eligibility dates back until ten years from the date of conviction.  \n"
            for label, section in sorted(future_eligible_charges, key=MarkdownSerializer._sort_future_eligible):
                listed_charges = MarkdownSerializer._build_listed_charges(section)
                text_block += "### " + label + "  \n" + listed_charges + "  \n\n"
            return text_block
        else:
            return ""

    @staticmethod
    def _sort_future_eligible(group):
        label = group[0]
        split = label.split(" ")
        for date_parts in zip(split, split[1:], split[2:]):
            date_string = " ".join(date_parts)
            try:
                date = datetime.strptime(date_string, "%b %d, %Y")
                return date.isoformat()
            except ValueError:
                pass
        return label

    @staticmethod
    def _gen_needs_more_analysis_block(record):
        needs_more_analysis_charges_tuples = [
            x for x in record["summary"]["charges_grouped_by_eligibility_and_case"] if x[0] == "Needs More Analysis"
        ]
        if len(needs_more_analysis_charges_tuples) > 0:
            text_block = "## Charges Needing More Analysis  \nAdditionally, you have charges for which the online records do not contain enough information to determine eligibility. If you are curious about the eligibility of these charges, please contact roe@qiu-qiulaw.com.  \n\n"
            listed_charges = MarkdownSerializer._build_listed_charges(needs_more_analysis_charges_tuples[0][1])
            text_block += listed_charges + "  \n\n"
            return text_block
        else:
            return ""
