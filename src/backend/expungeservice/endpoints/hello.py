"""Example endpoint."""

from flask.views import MethodView

class Hello(MethodView):

    def get(self):
        return 'Hello, world!'

def register(app):
    app.add_url_rule('/api/hello', view_func=Hello.as_view('hello'))
