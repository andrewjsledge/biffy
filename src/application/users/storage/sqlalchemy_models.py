__author__ = 'andrew'

from application import db
from application.users import constants as USER
from werkzeug.security import gen_salt
import datetime

user_service_accounts = db.Table('users_user_service_account',
    db.Column('service_account_id',
        db.Integer, db.ForeignKey('users_service_account.id')),
    db.Column('user_id',
        db.Integer, db.ForeignKey('users_user.id')),
)

class User(db.Model):
    __tablename__ = 'users_user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.SmallInteger, default=USER.USER)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(120))
    status = db.Column(db.SmallInteger, default=USER.NEW)

    service_accounts = db.relationship('ServiceAccount',
        secondary=user_service_accounts,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, first_name=None, last_name=None, email=None, phone=None,
                 status=USER.NEW):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.status = status

    def getStatus(self):
        return USER.STATUS[self.status]

    def getRole(self):
        return USER.ROLE[self.role]

    def __repr__(self):
        return '<User %r %r>' % (self.first_name, self.last_name)

class ServiceAccount(db.Model):
    __tablename__ = 'users_service_account'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(200))
    oauth_token = db.Column(db.String(200))
    oauth_secret = db.Column(db.String(200))
    service = db.Column(db.SmallInteger, default=USER.LOCAL)

    __table_args__ = (
        db.UniqueConstraint('name', 'service', name='_name_service_uc'),
    )

    def __init__(self, name=None, password=None, service=None):
        self.name = name
        self.password = password
        self.service = service

    def __repr__(self):
        return '<ServiceAccount %r %r>' % (self.name, self.service)

class Session(db.Model):
    __tablename__ = 'users_session'

    service_account = db.Column(db.ForeignKey('users_service_account.id'),
        unique=True)
    token = db.Column(db.String(64), primary_key=True)
    start_time = db.Column(db.DateTime)

    def __init__(self, service_account, token=None, start_time=None):
        self.service_account = service_account
        self.token = token
        if self.token is None:
            self.token = self._generate_token()
        self.start_time = start_time
        if self.start_time is None:
            self.start_time = datetime.datetime.now()

    def __repr__(self):
        return '<Session %r>' % self.token

    def _generate_token(self):
        return gen_salt(64)
