import jinja2
from typing import Dict

class MarkdownRenderer:
    def to_markdown(record: Dict, header: str) -> str:
        has_open_cases = ["open case" in error for error in record["errors"]]
        eligible_case_charges_tuples = [
            x for x in record["summary"]["charges_grouped_by_eligibility_and_case"] if x[0] == "Eligible Now"
        ]
        ineligible_case_charges_tuples = [
            x for x in record["summary"]["charges_grouped_by_eligibility_and_case"] if x[0] == "Ineligible"
        ]
        eligible_if_paid_case_charges_tuples = [
            x
            for x in record["summary"]["charges_grouped_by_eligibility_and_case"]
            if x[0] == "Eligible Now If Balance Paid"
        ]

        return MarkdownRenderer.render_without_request(
            "expungement_analysis_report.md",
            header=header, has_open_cases=has_open_cases, eligible_case_charges_tuples=eligible_case_charges_tuples,
            ineligible_case_charges_tuples=ineligible_case_charges_tuples,
            eligible_if_paid_case_charges_tuples=eligible_if_paid_case_charges_tuples
        )

    @staticmethod
    def render_without_request(template_name, **template_vars):
        """
        Usage is the same as flask.render_template:

        render_without_request('my_template.html', var1='foo', var2='bar')
        """
        env = jinja2.Environment(
            loader=jinja2.PackageLoader('expungeservice','templates'),
            trim_blocks=True
        )
        template = env.get_template(template_name)
        return template.render(**template_vars)
