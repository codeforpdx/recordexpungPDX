from flask.views import MethodView
from flask import request, current_app

from expungeservice.request import check_data_fields
from expungeservice.request.error import error
from expungeservice.crawler.crawler import Crawler
from expungeservice.expunger.expunger import Expunger
from expungeservice.endpoints.auth import user_auth_required
from expungeservice.serializer import ExpungeModelEncoder
from expungeservice.crypto import DataCipher
import json


class Search(MethodView):

    @user_auth_required
    def post(self):
        request_data = request.get_json()

        if request_data is None:
            error(400, "No json data in request body")

        check_data_fields(request_data, ["first_name", "last_name",
                                 "middle_name", "birth_date"])

        cipher = DataCipher(
            key=current_app.config.get("JWT_SECRET_KEY"))

        decrypted_credentials = cipher.decrypt(request.cookies["oeci_token"])

        crawler = Crawler()

        login_result = (
            decrypted_credentials["oeci_username"] == "username" and
            decrypted_credentials["oeci_password"] == "password")

        if login_result is False:
            error(401, "Attempted login to OECI failed")



        response_data = json.loads("""{"data": {"record": {
    "total_balance_due": 4550.4,
    "cases": [
        {
            "name": "Doe, John D",
            "birth_year": 1943,
            "case_number": "X0001",
            "citation_number": "C0001",
            "location": "Multnomah",
            "date": "Sat, 23 Mar 1963 00:00:00 GMT",
            "violation_type": "Offense Misdemeanor",
            "current_status": "Closed",
            "charges": [
                {
                    "name": "Driving Uninsured",
                    "statute": "806010",
                    "level": "Class B Felony",
                    "date": "Sun, 12 Mar 2017 00:00:00 GMT",
                    "disposition": {
                        "date": "Mon, 12 Jun 2017 00:00:00 GMT",
                        "ruling": "Convicted - Failure to Appear"
                    },
                    "expungement_result": {
                        "type_eligibility": false,
                        "type_eligibility_reason": "Ineligible under 137.225(5)",
                        "time_eligibility": null,
                        "time_eligibility_reason": null,
                        "date_of_eligibility": null
                    }
                },
                {
                    "name": "Violation Driving While Suspended or Revoked",
                    "statute": "811175",
                    "level": "Class B Felony",
                    "date": "Sun, 12 Mar 2017 00:00:00 GMT",
                    "disposition": {
                        "date": "Mon, 12 Jun 2017 00:00:00 GMT",
                        "ruling": "Dismissed"
                    },
                    "expungement_result": {
                        "type_eligibility": true,
                        "type_eligibility_reason": "Eligible under 137.225(1)(b)",
                        "time_eligibility": null,
                        "time_eligibility_reason": null,
                        "date_of_eligibility": null
                    }
                },
                {
                    "name": "Failure to Obey Traffic Control Device",
                    "statute": "811265",
                    "level": "Class B Felony",
                    "date": "Sun, 12 Mar 2017 00:00:00 GMT",
                    "disposition": {
                        "date": "Mon, 12 Jun 2017 00:00:00 GMT",
                        "ruling": "Dismissed"
                    },
                    "expungement_result": {
                        "type_eligibility": true,
                        "type_eligibility_reason": "Eligible under 137.225(1)(b)",
                        "time_eligibility": null,
                        "time_eligibility_reason": null,
                        "date_of_eligibility": null
                    }
                }
            ],
            "balance_due": 1516.8,
            "case_detail_link": "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=X0001"
        },
        {
            "name": "Doe, John D",
            "birth_year": 1943,
            "case_number": "X0002",
            "citation_number": "C0002",
            "location": "Multnomah",
            "date": "Thu, 11 Apr 1963 00:00:00 GMT",
            "violation_type": "Offense Felony",
            "current_status": "Closed",
            "charges": [
                {
                    "name": "Driving Uninsured",
                    "statute": "806010",
                    "level": "Class B Felony",
                    "date": "Sun, 12 Mar 2017 00:00:00 GMT",
                    "disposition": {
                        "date": "Mon, 12 Jun 2017 00:00:00 GMT",
                        "ruling": "Convicted - Failure to Appear"
                    },
                    "expungement_result": {
                        "type_eligibility": false,
                        "type_eligibility_reason": "Ineligible under 137.225(5)",
                        "time_eligibility": null,
                        "time_eligibility_reason": null,
                        "date_of_eligibility": null
                    }
                },
                {
                    "name": "Violation Driving While Suspended or Revoked",
                    "statute": "811175",
                    "level": "Class B Felony",
                    "date": "Sun, 12 Mar 2017 00:00:00 GMT",
                    "disposition": {
                        "date": "Mon, 12 Jun 2017 00:00:00 GMT",
                        "ruling": "Dismissed"
                    },
                    "expungement_result": {
                        "type_eligibility": true,
                        "type_eligibility_reason": "Eligible under 137.225(1)(b)",
                        "time_eligibility": null,
                        "time_eligibility_reason": null,
                        "date_of_eligibility": null
                    }
                },
                {
                    "name": "Failure to Obey Traffic Control Device",
                    "statute": "811265",
                    "level": "Class B Felony",
                    "date": "Sun, 12 Mar 2017 00:00:00 GMT",
                    "disposition": {
                        "date": "Mon, 12 Jun 2017 00:00:00 GMT",
                        "ruling": "Dismissed"
                    },
                    "expungement_result": {
                        "type_eligibility": true,
                        "type_eligibility_reason": "Eligible under 137.225(1)(b)",
                        "time_eligibility": null,
                        "time_eligibility_reason": null,
                        "date_of_eligibility": null
                    }
                }
            ],
            "balance_due": 1516.8,
            "case_detail_link": "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=X0002"
        },
        {
            "name": "Doe, John D",
            "birth_year": 1943,
            "case_number": "X0003",
            "citation_number": "",
            "location": "Multnomah",
            "date": "Sun, 01 Apr 2012 00:00:00 GMT",
            "violation_type": "Offense Misdemeanor",
            "current_status": "Closed",
            "charges": [
                {
                    "name": "Driving Uninsured",
                    "statute": "806010",
                    "level": "Class B Felony",
                    "date": "Sun, 12 Mar 2017 00:00:00 GMT",
                    "disposition": {
                        "date": "Mon, 12 Jun 2017 00:00:00 GMT",
                        "ruling": "Convicted - Failure to Appear"
                    },
                    "expungement_result": {
                        "type_eligibility": false,
                        "type_eligibility_reason": "Ineligible under 137.225(5)",
                        "time_eligibility": null,
                        "time_eligibility_reason": null,
                        "date_of_eligibility": null
                    }
                },
                {
                    "name": "Violation Driving While Suspended or Revoked",
                    "statute": "811175",
                    "level": "Class B Felony",
                    "date": "Sun, 12 Mar 2017 00:00:00 GMT",
                    "disposition": {
                        "date": "Mon, 12 Jun 2017 00:00:00 GMT",
                        "ruling": "Dismissed"
                    },
                    "expungement_result": {
                        "type_eligibility": true,
                        "type_eligibility_reason": "Eligible under 137.225(1)(b)",
                        "time_eligibility": null,
                        "time_eligibility_reason": null,
                        "date_of_eligibility": null
                    }
                },
                {
                    "name": "Failure to Obey Traffic Control Device",
                    "statute": "811265",
                    "level": "Class B Felony",
                    "date": "Sun, 12 Mar 2017 00:00:00 GMT",
                    "disposition": {
                        "date": "Mon, 12 Jun 2017 00:00:00 GMT",
                        "ruling": "Dismissed"
                    },
                    "expungement_result": {
                        "type_eligibility": true,
                        "type_eligibility_reason": "Eligible under 137.225(1)(b)",
                        "time_eligibility": null,
                        "time_eligibility_reason": null,
                        "date_of_eligibility": null
                    }
                }
            ],
            "balance_due": 1516.8,
            "case_detail_link": "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=X0003"
        }
    ],
    "errors": []
}

}}""")
        return response_data #Json-encoding happens automatically here


def register(app):
    app.add_url_rule("/api/search",
                     view_func=Search.as_view("search"))