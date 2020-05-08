from typing import Dict


class Serializer:
    @staticmethod
    def serialize(record: Dict, name: str, birth_date: str, officer: str) -> str:
        print(f"Processing {name}")
        title = f"# EXPUNGEMENT ANALYSIS REPORT  \n"
        name = f"Name: {name}  \n" if name else ""
        dob = f"DOB: {birth_date}  \n" if birth_date else ""
        officer = f"Officer: {officer}  \n" if officer else ""
        header = title + name + dob + officer
        open_cases_block = Serializer.gen_open_cases_block(record)
        eligible_charges_block = Serializer.gen_eligible_charges_block(record)
        ineligible_charges_block = Serializer.gen_ineligible_charges_block(record)
        future_eligible_block = Serializer.gen_future_eligible_block(record)
        needs_more_analysis_block = Serializer.gen_needs_more_analysis_block(record)
        return f"{header}  \n{open_cases_block}  \n{eligible_charges_block}  \n{ineligible_charges_block}  \n{future_eligible_block}  \n{needs_more_analysis_block}"

    @staticmethod
    def gen_open_cases_block(record):
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
    def gen_eligible_charges_block(record):
        eligible_charges = record["summary"]["eligible_charges_by_date"][0][
            1
        ]  # First item is the tuple ("now", charges)
        if eligible_charges:
            listed_charges = " - " + " \n - ".join(eligible_charges)
        else:
            listed_charges = "This client is not currently eligible to expunge any charges."
        return "## Charges Eligible Now  \n" + listed_charges + "  \n"

    @staticmethod
    def gen_ineligible_charges_block(record):
        ineligible_charges = record["summary"]["eligible_charges_by_date"][-1][
            1
        ]  # Last item is the tuple ("ineligible", charges)
        if ineligible_charges:
            ineligible_charges_string = " - " + "  \n - ".join(ineligible_charges)
            return f"## Ineligible Charges  \nThese convictions are not eligible for expungement at any time under the current law.  \n\n{ineligible_charges_string}  \n"
        else:
            return ""

    @staticmethod
    def gen_future_eligible_block(record):
        future_eligible_charges = record["summary"]["eligible_charges_by_date"][1:-1]
        text_block = "## Future Eligible Charges  \nThe following charges (dismissed and convicted) are eligible at the designated dates.  \n"
        if future_eligible_charges:
            for section in future_eligible_charges:
                listed_charges = " - " + "  \n - ".join(section[1])
                text_block += "### Eligible " + section[0] + "  \n" + listed_charges + "  \n\n"
            return text_block
        else:
            return ""

    @staticmethod
    def gen_needs_more_analysis_block(record):
        needs_more_analysis_charges = record["summary"]["needs_more_analysis_charges"]
        text_block = "## Charges Needing More Analysis  \nAdditionally, this client has charges for which the online records do not contain enough information to determine eligibility. If the client is curious about the eligibility of these charges, please have them contact michael@qiu-qiulaw.com.  \n\n"
        if needs_more_analysis_charges:
            listed_charges = " - " + "  \n - ".join(needs_more_analysis_charges)
            text_block += listed_charges + "  \n\n"
            return text_block
        else:
            return ""
