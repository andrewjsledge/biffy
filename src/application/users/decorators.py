__author__ = 'andrew'

from functools import wraps
from flask import g, flash, redirect, url_for, request
from application.users import constants as USER

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None and g.service_account is None:
            flash(USER.LOGIN_REQUIRED)
            return redirect(url_for('users.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'user') or g.user is None or g.user.getRole() != \
           USER.ADMIN:
            flash(USER.ACCESS_REQUIRED)
            return redirect(url_for('users.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function