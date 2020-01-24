import dataclasses

import flask
import expungeservice
from expungeservice.models.expungement_result import EligibilityStatus
from datetime import date


class ExpungeModelEncoder(flask.json.JSONEncoder):
    def record_to_json(self, record):
        return {
            "total_balance_due": record.total_balance_due,
            "cases": [self.case_to_json(case) for case in record.cases],
            "errors": record.errors,
            "summary": self.record_summary_to_json(record.summary)
        }

    def case_to_json(self, case):
        return {
            "name": case.name,
            "birth_year": case.birth_year,
            "case_number": case.case_number,
            "citation_number": case.citation_number,
            "location": case.location,
            "date": case.date,
            "violation_type": case.violation_type,
            "current_status": case.current_status,
            "charges": [self.charge_to_json(charge) for charge in case.charges],
            "balance_due": case.get_balance_due(),
            "probation_revoked": case.get_probation_revoked(),
            "case_detail_link": case.case_detail_link,
        }

    def charge_to_json(self, charge):
        disposition = self.disposition_to_json(charge.disposition) if charge.disposition else None
        return {
            "name": charge.name,
            "statute": charge.statute,
            "level": charge.level,
            "type_name": charge.type_name,
            "date": charge.date,
            "disposition": disposition,
            "expungement_result": self.expungement_result_to_json(charge.expungement_result),
        }

    def disposition_to_json(self, disposition):
        return {"date": disposition.date, "ruling": disposition.ruling, "status": disposition.status, "amended": disposition.amended}

    def expungement_result_to_json(self, expungement_result):
        return {
            "type_eligibility": expungement_result.type_eligibility,
            "time_eligibility": expungement_result.time_eligibility,
            "charge_eligibility": expungement_result.charge_eligibility,
        }

    def record_summary_to_json(self, record_summary):
        return {
            "total_charges": record_summary.total_charges,
            "cases_sorted": record_summary.cases_sorted,
            "eligible_charges": record_summary.eligible_charges,
            "county_balances": record_summary.county_balances,
            "total_balance_due": record_summary.total_balance_due,
            "total_cases": record_summary.total_cases,
        }

    def default(self, o):
        if isinstance(o, expungeservice.models.record.Record):
            return self.record_to_json(o)

        elif isinstance(o, date):
            return o.strftime("%b %-d, %Y")

        else:
            return flask.json.JSONEncoder.default(self, o)
