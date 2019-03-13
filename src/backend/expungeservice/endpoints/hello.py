"""Example endpoint."""

from flask.views import MethodView

class Hello(MethodView):

    def get(self):
        return 'Hello, world!'

class Register(MethodView):

    def get(self):
        return "registration endpoint!"

def register(app):
    app.add_url_rule('/hello', view_func=Hello.as_view('hello'))

    app.add_url_rule('/register', view_func=Register.as_view('register'))


