from flask import request, render_template, flash, g, session,\
    redirect, url_for, Blueprint
from flask.ext.admin.contrib.sqlamodel import ModelView

from application.decorators import load_session
from application.views import WebView
from application.users import constants as USER
from application.users.decorators import admin_required
from application.users.storage import get_session, get_service_account, \
    get_user
from application import app_admin


class SessionView(ModelView):
    list_columns = ('token', 'start_time',)
    rename_columns = dict(token='Token hash', start_time='Session start')

    @load_session
    def is_accessible(self):
        return g.is_admin