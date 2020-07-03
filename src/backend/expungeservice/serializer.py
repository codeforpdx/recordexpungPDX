from dataclasses import asdict

import flask
from expungeservice.util import DateWithFuture as date

from expungeservice.models.record import Record
from expungeservice.models.record_summary import RecordSummary


class ExpungeModelEncoder(flask.json.JSONEncoder):
    def record_summary_to_json(self, record_summary):
        return {
            **self.record_to_json(record_summary.record),
            **{
                "summary": {
                    "total_charges": record_summary.total_charges,
                    "eligible_charges_by_date": record_summary.eligible_charges_by_date,
                    "county_balances": record_summary.county_balances,
                    "total_balance_due": record_summary.total_balance_due,
                    "total_cases": record_summary.total_cases,
                },
                "questions": record_summary.questions,
            },
        }

    def record_to_json(self, record):
        return {
            "total_balance_due": record.total_balance_due,
            "cases": [self.case_to_json(case) for case in record.cases],
            "errors": record.errors,
        }

    def case_to_json(self, case):
        return {
            **self.case_summary_to_json(case.summary),
            "charges": [self.charge_to_json(charge) for charge in case.charges],
        }

    def case_summary_to_json(self, case):
        return {
            "name": case.name,
            "birth_year": case.birth_year,
            "case_number": case.case_number,
            "citation_number": case.citation_number,
            "location": case.location,
            "date": case.date,
            "violation_type": case.violation_type,
            "current_status": case.current_status + " (Closed)" if case.closed() else " (Open)",
            "balance_due": case.get_balance_due(),
            "case_detail_link": case.case_detail_link,
            "edit_status": case.edit_status,
        }

    def charge_to_json(self, charge):
        return {
            "ambiguous_charge_id": charge.ambiguous_charge_id,
            "case_number": charge.case_number,
            "date": charge.date,
            "disposition": charge.disposition,
            "expungement_result": charge.expungement_result,
            "id": charge.id,
            "level": charge.level,
            "name": charge.name,
            "probation_revoked": charge.probation_revoked,
            "statute": charge.statute,
            "type_name": charge.charge_type.type_name,
            "expungement_rules": charge.charge_type.expungement_rules,
            "edit_status": charge.edit_status,
        }

    def default(self, o):
        if isinstance(o, RecordSummary):
            return self.record_summary_to_json(o)
        elif isinstance(o, Record):
            return self.record_to_json(o)
        elif isinstance(o, date):
            return o.strftime("%b %-d, %Y")
        else:
            return flask.json.JSONEncoder.default(self, o)
