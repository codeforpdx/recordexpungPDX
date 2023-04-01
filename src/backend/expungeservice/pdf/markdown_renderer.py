import jinja2
from expungeservice.pdf.markdown_serializer import MarkdownSerializer
from typing import Dict, List, Optional, Tuple

class MarkdownRenderer:
    @staticmethod
    def to_markdown(record: Dict, header: Optional[str] = None, aliases: List[Dict] = []) -> str:
        mapped_aliases = map(MarkdownRenderer.name_and_birth_info, aliases)
        has_open_cases = ["open case" in error for error in record["errors"]]
        eligible_case_charges = [
            x for x in record["summary"]["charges_grouped_by_eligibility_and_case"] if x[0] == "Eligible Now"
        ]
        ineligible_case_charges = [
            x for x in record["summary"]["charges_grouped_by_eligibility_and_case"] if x[0] == "Ineligible"
        ]
        eligible_if_paid_case_charges = [
            x
            for x in record["summary"]["charges_grouped_by_eligibility_and_case"]
            if x[0] == "Eligible Now If Balance Paid"
        ]
        eligible_charges_by_date = record["summary"]["charges_grouped_by_eligibility_and_case"]
        future_eligible_charges = [
            (key, eligible_charges_for_date)
            for key, eligible_charges_for_date in eligible_charges_by_date
            if key not in ["Eligible Now", "Ineligible", "Needs More Analysis", "Eligible Now If Balance Paid"]
        ]
        needs_more_analysis_charges = [
            x for x in record["summary"]["charges_grouped_by_eligibility_and_case"] if x[0] == "Needs More Analysis"
        ]

        return MarkdownRenderer.render_without_request(
            "expungement_analysis_report.md",
            header=header, aliases=mapped_aliases, has_open_cases=has_open_cases,
            eligible_case_charges=eligible_case_charges,
            ineligible_case_charges=ineligible_case_charges,
            eligible_if_paid_case_charges=eligible_if_paid_case_charges,
            future_eligible_charges=sorted(future_eligible_charges, key=MarkdownSerializer._sort_future_eligible),
            needs_more_analysis_charges=needs_more_analysis_charges
        )

    @staticmethod
    def render_without_request(template_name, **template_vars):
        """
        Usage is the same as flask.render_template:

        render_without_request('my_template.html', var1='foo', var2='bar')
        """
        env = jinja2.Environment(
            loader=jinja2.PackageLoader('expungeservice','templates'),
            trim_blocks=True, lstrip_blocks=True
        )
        template = env.get_template(template_name)
        return template.render(**template_vars)

    @staticmethod
    def name_and_birth_info(alias: Dict) -> Tuple[str, Optional[str]]:
        name = ' '.join([
            alias.get('first_name', ''),
            alias.get('middle_name',''),
            alias.get('last_name','')
        ]).upper()
        return (name, alias.get('birth_date'))
