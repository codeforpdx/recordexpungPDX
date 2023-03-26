import jinja2
from typing import Dict

class MarkdownRenderer:
    def to_markdown(record: Dict, header: str) -> str:
        has_open_cases = ["open case" in error for error in record["errors"]]

        return MarkdownRenderer.render_without_request(
            "expungement_analysis_report.md",
            header=header, has_open_cases=has_open_cases
        )

    @staticmethod
    def render_without_request(template_name, **template_vars):
        """
        Usage is the same as flask.render_template:

        render_without_request('my_template.html', var1='foo', var2='bar')
        """
        env = jinja2.Environment(
            loader=jinja2.PackageLoader('expungeservice','templates')
        )
        template = env.get_template(template_name)
        return template.render(**template_vars)
