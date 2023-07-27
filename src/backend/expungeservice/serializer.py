from dataclasses import is_dataclass, asdict

from expungeservice.util import DateWithFuture as date
from expungeservice.models.record import Record
from expungeservice.models.record_summary import RecordSummary, CountyFines
from json import JSONEncoder


class ExpungeModelEncoder(JSONEncoder):
    def record_summary_to_json(self, record_summary):
        record_summary = {
            **self.record_to_json(record_summary.record),
            **{
                "summary": {
                    "total_charges": record_summary.total_charges,
                    "charges_grouped_by_eligibility_and_case": record_summary.charges_grouped_by_eligibility_and_case,
                    "total_cases": record_summary.total_cases,
                    "county_fines": record_summary.county_fines,
                    "total_fines_due": record_summary.total_fines_due,
                },
                "questions": record_summary.questions,
            },
        }
        return record_summary

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
            "birth_year": case.birth_year if case.birth_year else "",
            "case_number": case.case_number,
            "citation_number": case.citation_number,
            "location": case.location,
            "date": case.date,
            "violation_type": case.violation_type,
            "current_status": case.current_status
            + (
                "" if case.current_status.lower() in ["open", "closed"] else " (Closed)" if case.closed() else " (Open)"
            ),
            "balance_due": case.get_balance_due(),
            "case_detail_link": case.case_detail_link,
            "district_attorney_number": case.district_attorney_number,
            "sid": case.sid,
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

    def county_fines_to_json(self, county_fines):
        return {
            "county_name": county_fines.county_name,
            "case_fines": county_fines.case_fines,
            "total_fines_due": county_fines.total_fines_due,
        }

    def default(self, o):
        if isinstance(o, RecordSummary):
            return self.record_summary_to_json(o)
        elif isinstance(o, Record):
            return self.record_to_json(o)
        elif isinstance(o, CountyFines):
            return self.county_fines_to_json(o)
        elif isinstance(o, date):
            return o.strftime("%b %-d, %Y")
        elif is_dataclass(o):
            return asdict(o)
        else:
            return JSONEncoder.default(self, o)
