import pytest
from flask import json

from expungeservice.endpoints.search import Disambiguate
from expungeservice.models.record import Question
from tests.factories.crawler_factory import CrawlerFactory
from tests.fixtures.case_details import CaseDetails
from tests.fixtures.john_doe import JohnDoe

DUII_SEARCH_RESPONSE = {
    "data": {
        "record": {
            "cases": [
                {
                    "balance_due": 0.0,
                    "birth_year": 1969,
                    "case_detail_link": "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=CASEJD1",
                    "case_number": "CASEJD1",
                    "charges": [
                        {
                            "ambiguous_charge_id": "CASEJD1-1",
                            "date": "Nov 7, 1997",
                            "disposition": {
                                "amended": False,
                                "date": "Nov 10, 1997",
                                "ruling": "Dismissed",
                                "status": "Dismissed",
                            },
                            "expungement_result": {
                                "charge_eligibility": {
                                    "label": "Possibly Eligible Now (review)",
                                    "status": "Possibly eligible",
                                },
                                "time_eligibility": {
                                    "date_will_be_eligible": "Dec 31, 9999",
                                    "reason": "Never. Type ineligible charges are always time ineligible. ⬥ Eligible now",
                                    "status": "Ineligible",
                                },
                                "type_eligibility": {
                                    "reason": "137.225(8)(b) - Diverted DUIIs are ineligible ⬥ Dismissals are generally eligible under 137.225(1)(b)",
                                    "status": "Needs more analysis",
                                },
                            },
                            "level": "Misdemeanor Class A",
                            "name": "DUII",
                            "statute": "813010",
                            "type_name": "Diverted DUII ⬥ Dismissed Criminal Charge",
                        }
                    ],
                    "citation_number": "CASEJD1",
                    "current_status": "Closed",
                    "date": "Sep 5, 2008",
                    "location": "Multnomah",
                    "name": "DOE, JOHN",
                    "probation_revoked": None,
                    "violation_type": "Misdemeanor",
                }
            ],
            "errors": [],
            "questions": [
                {
                    "ambiguous_charge_id": "CASEJD1-1",
                    "answer": "",
                    "options": {"No": "CASEJD1-1-1", "Yes": "CASEJD1-1-0"},
                    "question": "Was the charge dismissed pursuant to a court-ordered diversion program?",
                }
            ],
            "summary": {
                "cases_sorted": {
                    "fully_eligible": [],
                    "fully_ineligible": [],
                    "other": ["CASEJD1"],
                    "partially_eligible": [],
                },
                "county_balances": [{"balance": 0.0, "county_name": "Multnomah"}],
                "eligible_charges_by_date": [["now", []]],
                "total_balance_due": 0.0,
                "total_cases": 1,
                "total_charges": 1,
            },
            "total_balance_due": 0.0,
        }
    }
}
DIVERTED_RESPONSE = {
    "data": {
        "record": {
            "cases": [
                {
                    "balance_due": 0.0,
                    "birth_year": 1969,
                    "case_detail_link": "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=CASEJD1",
                    "case_number": "CASEJD1",
                    "charges": [
                        {
                            "ambiguous_charge_id": "CASEJD1-1",
                            "date": "Nov 7, 1997",
                            "disposition": {
                                "amended": False,
                                "date": "Nov 10, 1997",
                                "ruling": "Dismissed",
                                "status": "Dismissed",
                            },
                            "expungement_result": {
                                "charge_eligibility": {"label": "Ineligible", "status": "Ineligible"},
                                "time_eligibility": {
                                    "date_will_be_eligible": "Dec 31, 9999",
                                    "reason": "Never. Type ineligible charges are always time ineligible.",
                                    "status": "Ineligible",
                                },
                                "type_eligibility": {
                                    "reason": "137.225(8)(b) - Diverted DUIIs are ineligible",
                                    "status": "Ineligible",
                                },
                            },
                            "level": "Misdemeanor Class A",
                            "name": "DUII",
                            "statute": "813010",
                            "type_name": "Diverted DUII",
                        }
                    ],
                    "citation_number": "CASEJD1",
                    "current_status": "Closed",
                    "date": "Sep 5, 2008",
                    "location": "Multnomah",
                    "name": "DOE, JOHN",
                    "probation_revoked": None,
                    "violation_type": "Misdemeanor",
                }
            ],
            "errors": [],
            "questions": [
                {
                    "ambiguous_charge_id": "CASEJD1-1",
                    "answer": "CASEJD1-1-0",
                    "options": {"No": "CASEJD1-1-1", "Yes": "CASEJD1-1-0"},
                    "question": "Was the charge dismissed pursuant to a court-ordered diversion program?",
                }
            ],
            "summary": {
                "cases_sorted": {
                    "fully_eligible": [],
                    "fully_ineligible": ["CASEJD1"],
                    "other": [],
                    "partially_eligible": [],
                },
                "county_balances": [{"balance": 0.0, "county_name": "Multnomah"}],
                "eligible_charges_by_date": [["now", []]],
                "total_balance_due": 0.0,
                "total_cases": 1,
                "total_charges": 1,
            },
            "total_balance_due": 0.0,
        }
    }
}


@pytest.fixture
def record_with_single_duii():
    return CrawlerFactory.create_ambiguous_record_with_questions(
        record=JohnDoe.SINGLE_CASE_RECORD, cases={"CASEJD1": CaseDetails.CASE_WITH_SINGLE_DUII,},
    )


def test_disambiguate_endpoint_with_no_answers(record_with_single_duii):
    ambiguous_record = record_with_single_duii[1]
    questions = json.loads(json.dumps(record_with_single_duii[2]))
    response = Disambiguate.build_response(ambiguous_record, questions)
    response_as_dict = json.loads(response)
    assert response_as_dict == DUII_SEARCH_RESPONSE


def test_disambiguate_endpoint_with_diverted_answer(record_with_single_duii):
    ambiguous_record = record_with_single_duii[1]
    answers = [
        Question(
            ambiguous_charge_id="CASEJD1-1",
            question="Was the charge dismissed pursuant to a court-ordered diversion program?",
            options={"Yes": "CASEJD1-1-0", "No": "CASEJD1-1-1"},
            answer="CASEJD1-1-0",
        )
    ]
    questions = json.loads(json.dumps(answers))
    response = Disambiguate.build_response(ambiguous_record, questions)
    response_as_dict = json.loads(response)
    assert response_as_dict == DIVERTED_RESPONSE
