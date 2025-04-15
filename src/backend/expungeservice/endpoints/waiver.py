from expungeservice.endpoints.demo import Demo
from flask.views import MethodView
from flask import request, send_file

from expungeservice.endpoints.search import Search
from expungeservice.waiver_form_filling import WaiverFormFilling


class WaiverPDF(MethodView):
    def post(self):
        request_data = request.get_json()
        user_information = request_data.get("userInformation")
        waiver_information = request_data.get("waiverInformation")
        demo = request_data.get("demo")
        search = Demo if demo else Search
        record_summary = search().build_response()  # type: ignore
        zip_path, zip_name = WaiverFormFilling.build_zip(record_summary, user_information, waiver_information)
        return send_file(zip_path, as_attachment=True, attachment_filename=zip_name)

def register(app):
    app.add_url_rule("/api/waiver-packet", view_func=WaiverPDF.as_view("waiver-packet"))
