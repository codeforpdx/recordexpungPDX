from typing import Dict


class Serializer:
    @staticmethod
    def serialize(alias, record: Dict) -> str:
        print(f"Processing {alias}")
        title = f"# EXPUNGEMENT ANALYSIS REPORT  \nName: {alias['first_name'].upper()} {alias['last_name'].upper()}  \nDOB: {alias['birth_date'].upper()}\n"
        open_cases_block = Serializer.gen_open_cases_block(record)
        eligible_charges_block = Serializer.gen_eligible_charges_block(record)
        ineligible_charges_block = Serializer.gen_ineligible_charges_block(record)
        future_eligible_block = Serializer.gen_future_eligible_block(record)
        # needs_more_analysis_block = gen_needs_more_analysis_block(record)
        return f"{title}  \n{open_cases_block}  \n{eligible_charges_block}  \n{ineligible_charges_block}  \n{future_eligible_block}"

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
            listed_charges = "  \n".join(eligible_charges)
        else:
            listed_charges = "This client is not currently eligible to expunge any charges.  \n"
        return "## Charges Eligible Now  \n" + listed_charges

    @staticmethod
    def gen_ineligible_charges_block(record):
        ineligible_charges = record["summary"]["eligible_charges_by_date"][-1][
            1
        ]  # Last item is the tuple ("ineligible", charges)
        if ineligible_charges:
            ineligible_charges_string = "  \n".join(ineligible_charges)
            return f"## Ineligible Charges  \nThese convictions are not eligible for expungement at any time under the current law.  \n\n{ineligible_charges_string}"
        else:
            return ""

    @staticmethod
    def gen_future_eligible_block(record):
        future_eligible_charges = record["summary"]["eligible_charges_by_date"][1:-1]
        text_block = "## Future Eligible Charges  \nThe following charges (dismissed and convicted) are eligible at the designated dates.  \n"
        if future_eligible_charges:
            for section in future_eligible_charges:
                listed_charges = "  \n".join(section[1])
                text_block += "### Eligible " + section[0] + "  \n" + listed_charges + "  \n\n"
            return text_block
        else:
            return ""
