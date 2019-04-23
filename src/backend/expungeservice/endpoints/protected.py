# TODO remove this file later. This is just an example to test authentication

from flask.views import MethodView
from .auth import auth_required

class ProtectedView(MethodView):
    @auth_required
    def get(self):
        return 'Protected View'

def register(app):
    app.add_url_rule('/api/v0.1/test/protected', view_func=ProtectedView.as_view('protected'))
