from application.users.storage import Session
from application.admin.views import SessionView

from application import app_admin, db

app_admin.add_view(SessionView(Session, db.session))
