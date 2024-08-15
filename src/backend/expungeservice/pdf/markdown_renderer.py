import jinja2
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class MarkdownRenderer:
    @staticmethod
    def to_markdown(record: Dict, header: Optional[str] = None, aliases: List[Dict] = None) -> str:
        mapped_aliases = map(MarkdownRenderer._name_and_birth_info, aliases or [])
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
        
        county_fines = [x for x in record["summary"]["county_fines"]]
        
        eligible_charges_by_date = record["summary"]["charges_grouped_by_eligibility_and_case"]
        future_eligible_charges = [
            (key, eligible_charges_for_date)
            for key, eligible_charges_for_date in eligible_charges_by_date
            if key not in ["Eligible Now", "Ineligible", "Needs More Analysis", "Eligible Now If Balance Paid"]
        ]
        needs_more_analysis_charges = [
            x for x in record["summary"]["charges_grouped_by_eligibility_and_case"] if x[0] == "Needs More Analysis"
        ]

        return MarkdownRenderer._render_without_request(
            "expungement_analysis_report.md.j2",
            header=header, aliases=mapped_aliases, has_open_cases=has_open_cases,
            eligible_case_charges=eligible_case_charges,
            ineligible_case_charges=ineligible_case_charges,
            eligible_if_paid_case_charges=eligible_if_paid_case_charges,
            future_eligible_charges=sorted(future_eligible_charges, key=MarkdownRenderer._sort_future_eligible),
            needs_more_analysis_charges=needs_more_analysis_charges,
            county_fines = county_fines,
        )

    @staticmethod
    def _render_without_request(template_name, **template_vars):
        """
        Usage is the same as flask.render_template:

        render_without_request('my_template.html', var1='foo', var2='bar')
        """
        env = jinja2.Environment(
            loader=jinja2.PackageLoader('expungeservice','templates'),
            trim_blocks=True, lstrip_blocks=True, autoescape=True
        )
        template = env.get_template(template_name)
        return template.render(**template_vars)

    @staticmethod
    def _name_and_birth_info(alias: Dict) -> Tuple[str, Optional[str]]:
        name = ' '.join([
            alias.get('first_name', ''),
            alias.get('middle_name',''),
            alias.get('last_name','')
        ]).upper()
        return (name, alias.get('birth_date'))

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