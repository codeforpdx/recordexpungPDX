import flask
from expungeservice.util import DateWithFuture as date

from expungeservice.models.record import Record
from expungeservice.models.record_summary import RecordSummary, CountyFines


class ExpungeModelEncoder(flask.json.JSONEncoder):
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
                    "sb819_analysis": self.sb819_analysis_to_json(record_summary.sb819_analysis),
                },
                "questions": record_summary.questions,
            },
        }
        return record_summary

    def sb819_analysis_to_json(self, analysis):
        return {
            "counties_analyzed": list(analysis.counties_analyzed),
            "has_analyzed_charges": analysis.has_analyzed_charges,
            "has_possibly_eligible": analysis.has_possibly_eligible,
            "sections": [
                {"status": status, "charge_ids": [a.ambiguous_charge_id for a in analyses]}
                for status, analyses in analysis.sections
            ],
            "charges": {
                charge_analysis.ambiguous_charge_id: self.sb819_charge_analysis_to_json(charge_analysis)
                for charge_analysis in analysis.charge_analyses
            },
        }

    def sb819_charge_analysis_to_json(self, charge_analysis):
        return {
            "ambiguous_charge_id": charge_analysis.ambiguous_charge_id,
            "case_number": charge_analysis.case_number,
            "charge_name": charge_analysis.charge_name,
            "status": charge_analysis.status,
            "main_criteria": [self.sb819_criterion_result_to_json(r) for r in charge_analysis.main_criterion_results],
            "pathways": [self.sb819_pathway_result_to_json(p) for p in charge_analysis.pathway_results],
        }

    def sb819_pathway_result_to_json(self, pathway_result):
        return {
            "pathway": pathway_result.pathway,
            "status": pathway_result.status,
            "criteria": [self.sb819_criterion_result_to_json(r) for r in pathway_result.criterion_results],
        }

    def sb819_criterion_result_to_json(self, criterion_result):
        criterion = criterion_result.criterion
        return {
            "key": criterion.key,
            "scope": criterion.scope,
            "is_gate": criterion.is_gate,
            "is_screenable": criterion.is_screenable,
            "name": criterion.name,
            "description": criterion.description,
            "citation": criterion.citation,
            "determination": criterion.determination,
            "pathway": criterion.pathway,
            "outcome": criterion_result.outcome,
            "explanation": criterion_result.explanation,
            "question": self.sb819_question_to_json(criterion_result.question),
        }

    def sb819_question_to_json(self, question):
        if not question:
            return None
        return {
            "text": question.text,
            "if_yes": question.if_yes,
            "if_no": question.if_no,
            "note": question.note,
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
            "restitution": case.restitution,
            "edit_status": case.edit_status,
            "set_aside_motion": self.set_aside_motion_to_json(case.set_aside_motion),
        }

    def set_aside_motion_to_json(self, motion):
        if not motion:
            return None
        return {"status": motion.status, "filed_date": motion.filed_date, "resolved_date": motion.resolved_date}

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
        else:
            return flask.json.JSONEncoder.default(self, o)
