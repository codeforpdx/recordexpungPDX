from datetime import datetime
from typing import Dict


class MarkdownSerializer:
    @staticmethod
    def to_markdown(record: Dict, header: str) -> str:
        open_cases_block = MarkdownSerializer._gen_open_cases_block(record)
        eligible_charges_block = MarkdownSerializer._gen_eligible_charges_block(record)
        ineligible_charges_block = MarkdownSerializer._gen_ineligible_charges_block(record)
        future_eligible_block = MarkdownSerializer._gen_future_eligible_block(record)
        needs_more_analysis_block = MarkdownSerializer._gen_needs_more_analysis_block(record)
        return f"{header}  \n{open_cases_block}  \n{eligible_charges_block}  \n{ineligible_charges_block}  \n{future_eligible_block}  \n{needs_more_analysis_block}"

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
            return (
                "This person has another case open. "
                "A person is not eligible while they have open cases "
                "(cases which have yet to be either dismissed or convicted). "
                "The analysis below assumes that the open cases will be dismissed. "
                "If the client receives a conviction on the open case, "
                "the eligibility dates below should be changed to ten years from the date of the conviction in the open case."
                "  \n\n"
            )
        else:
            return ""

    @staticmethod
    def _gen_eligible_charges_block(record):
        eligible_charges = record["summary"]["eligible_charges_by_date"].get("Eligible Now")
        if eligible_charges:
            charges = [charge_tuple[1] for charge_tuple in eligible_charges]
            listed_charges = " - " + " \n - ".join(charges)
        else:
            listed_charges = "This client is not currently eligible to expunge any charges."
        return "## Charges Eligible Now  \n" + listed_charges + "  \n"

    @staticmethod
    def _gen_ineligible_charges_block(record):
        ineligible_charges = record["summary"]["eligible_charges_by_date"].get("Ineligible")
        if ineligible_charges:
            charges = [charge_tuple[1] for charge_tuple in ineligible_charges]
            charges_string = " - " + "  \n - ".join(charges)
            return f"## Ineligible Charges  \nThese convictions are not eligible for expungement at any time under the current law.  \n\n{charges_string}  \n"
        else:
            return ""

    @staticmethod
    def _gen_future_eligible_block(record):
        eligible_charges_by_date = record["summary"]["eligible_charges_by_date"]
        future_eligible_charges = [
            (key, eligible_charges_by_date[key])
            for key in eligible_charges_by_date.keys()
            if key not in ["Eligible Now", "Ineligible", "Needs More Analysis"]
        ]
        if future_eligible_charges:
            text_block = "## Future Eligible Charges  \nThe following charges (dismissed and convicted) are eligible at the designated dates.  \n"
            for label, section in sorted(future_eligible_charges, key=MarkdownSerializer._sort_future_eligible):
                charges = [charge_tuple[1] for charge_tuple in section]
                listed_charges = " - " + "  \n - ".join(charges)
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
        needs_more_analysis_charges = record["summary"]["eligible_charges_by_date"].get("Needs More Analysis")
        if needs_more_analysis_charges:
            charges = [charge_tuple[1] for charge_tuple in needs_more_analysis_charges]
            text_block = "## Charges Needing More Analysis  \nAdditionally, this client has charges for which the online records do not contain enough information to determine eligibility. If the client is curious about the eligibility of these charges, please have them contact michael@qiu-qiulaw.com.  \n\n"
            listed_charges = " - " + "  \n - ".join(charges)
            text_block += listed_charges + "  \n\n"
            return text_block
        else:
            return ""
