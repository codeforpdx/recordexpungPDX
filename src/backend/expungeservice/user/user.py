import functools
from dataclasses import dataclass

from flask import current_app, abort
from flask_login import login_user, UserMixin, current_user


@dataclass
class User:
    user_id : str
    email : str
    name : str
    group_name : str
    admin : bool

    @staticmethod
    def login_user(user):
        login_user(user, remember=True)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        return self.admin

    def get_id(self):
        return self.user_id

def admin_login_required(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return func(*args, **kwargs)
        elif current_user.is_authenticated:
            abort(403)
        else:
            return current_app.login_manager.unauthorized()
    return decorated_view
