from flask import session, g

def load_session(f):
    def decorator(*args, **kwargs):
        g.user = None
        g.service_account = None
        g.is_admin = False
        if 'session_token' in session:
            import application.users.constants as USER
            from application.users.storage import get_service_account, \
                get_session, get_user
            sess = get_session(token=session['session_token'])
            if sess is not None:
                service_account = get_service_account(id=sess.service_account)
                if service_account is not None:
                    g.service_account = service_account
                    user = get_user(service_account=service_account)
                    if user is not None:
                        g.user = user
                        for test_service_account in g.user.service_accounts:
                            if test_service_account.service == USER.LOCAL:
                                g.username = test_service_account.name
                        if user.getRole() == USER.ADMIN:
                            g.is_admin = True
        return f(*args, **kwargs)
    return decorator