from flask.views import MethodView
from flask import make_response

class OeciLogout(MethodView):
    def post(self):
      response = make_response()
      response.delete_cookie("oeci_token")
      return response


def register(app):
    app.add_url_rule("/api/oeci_logout", view_func=OeciLogout.as_view("oeci_logout"))