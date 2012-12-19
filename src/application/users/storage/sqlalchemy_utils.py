from application import db
from application.users import constants as USER
from application.users.storage.sqlalchemy_models import Session, \
    ServiceAccount, User

def get_session(token=None, service_account=None):
    if token:
        return Session.query.filter_by(token=token).first()
    elif service_account:
        return Session.query.filter_by(service_account=service_account).first()
    else:
        return None

def has_session(service_account_id):
    sess = db.session.query(Session).filter(
        Session.service_account==service_account_id).all()
    return sess is not None

def create_session(service_account):
    if has_session(service_account.id):
        remove_session(service_account.id)
    s = Session(service_account=service_account.id)
    db.session.add(s)
    db.session.commit()
    return s.token

def remove_session(service_account_id):
    s = db.session.query(Session).filter(
            Session.service_account==service_account_id).all()
    for k in s:
        db.session.delete(k)
    db.session.commit()

def get_service_account(id=None, name=None, service=None):
    if id:
        service_account = ServiceAccount.query.filter_by(id=id).first()
    elif name and not service:
        service_account = ServiceAccount.query.filter_by(name=name).first()
    elif name and service:
        service_account = ServiceAccount.query.filter_by(name=name,
            service=service).first()
    else:
        service_account = None
    return service_account

def get_user(username=None, service_account=None):
    if username:
        return db.session.query(User).filter(
            ServiceAccount.name==username,
            ServiceAccount.service==USER.LOCAL).first()
    if service_account:
        if type(service_account) == ServiceAccount:
            return db.session.query(User).filter(
                ServiceAccount.id==service_account.id).first()
        else:
            raise TypeError("%r is not a valid ServiceAccount object." %
                            service_account)

def create_service_account(name=None, password=None, oauth_token=None,
                           oauth_secret=None, service=None):
    service_account = ServiceAccount(
        name=name,
        password=password,
        service=service)
    service_account.oauth_token=oauth_token
    service_account.oauth_secret=oauth_secret
    db.session.add(service_account)
    db.session.commit()
    return service_account

def connect_service_account_to_user(user, service_account):
    user.service_accounts.append(service_account)
    db.session.merge(user)
    db.session.commit()

def create_user(first_name=None, last_name=None, role=None, email=None,
                phone=None, status=None):
    user = User(first_name, last_name, email, phone, status)
    db.session.add(user)
    db.session.commit()
    return user