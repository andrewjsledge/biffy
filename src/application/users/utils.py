from flask_oauth import OAuth, OAuthRemoteApp, OAuthException
from functools import wraps
from flask import request, session

class BiffyOAuthRemoteApp(OAuthRemoteApp):

    def get_request_token(self, token=None):
        import oauth2
        import inspect
        assert self.tokengetter_func is not None, 'missing tokengetter function'
        arg_tuple = inspect.getargspec(self.tokengetter_func)
        if 'self' in arg_tuple[0]:
            index = arg_tuple[0].index('self')
            arg = arg_tuple[0][index]
            rv = self.tokengetter_func(arg, *(token and (token,) or ()))
        else:
            rv = self.tokengetter_func(*(token and (token,) or ()))
        if rv is None:
            rv = session.get(self.name + '_oauthtok')
            if rv is None:
                raise OAuthException('No token available', type='token_missing')
        return oauth2.Token(*rv)

    def authorized_handler(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'oauth_verifier' in request.args:
                data = self.handle_oauth1_response()
            elif 'code' in request.args:
                data = self.handle_oauth2_response()
            else:
                data = self.handle_unknown_response()
            self.free_request_token()
            from .views import oauth_login_handlers
            for arg in args:
                for handler in oauth_login_handlers:
                    if isinstance(arg, handler):
                        return f(*(args), data=data, **kwargs)
            return f(*((data,) + args), **kwargs)
        return decorated

class BiffyOAuth(OAuth):
    def remote_app(self, name, register=True, **kwargs):
        app = BiffyOAuthRemoteApp(self, name, **kwargs)
        if register:
            assert name not in self.remote_apps,\
            'application already registered'
            self.remote_apps[name] = app
        return app