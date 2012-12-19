from flask import request, render_template, flash, g, session,\
    redirect, url_for, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash

from application import app
from application.views import WebView, APIView
from application.utils import register_module_web_route
from application.decorators import load_session

from application.users.forms import RegisterForm, ProfileForm, EmailLoginForm
from application.users.decorators import login_required
from application.users.storage import create_session, remove_session, \
    get_session, get_service_account, get_user, create_user, \
    create_service_account, connect_service_account_to_user
from application.users import constants as USER, mod, twitter, facebook, google

oauth_login_handlers = list([])

class Home(WebView):

    @login_required
    def dispatch_request(self, *args, **kwargs):
        service_account_ids = [s.service for s in g.user.service_accounts]
        form = ProfileForm(obj=g.user)
        if request.method == "POST":
            if form.validate_on_submit():
                flash(USER.PROFILE_UPDATE_SUCCESSFUL, 'success')
            else:
                flash(USER.PROFILE_UPDATE_FAILED, 'error')
        return render_template(self.template_name, user=g.user,
            service_account=g.service_account,
            service_account_ids=service_account_ids,
            form=form,
        )

class Login(WebView):

    def dispatch_request(self, *args, **kwargs):
        form = EmailLoginForm(request.form)
        if request.method == "POST":
            if form.validate_on_submit():
                service_account = get_service_account(name=form.email.data,
                    service=USER.LOCAL)
                if service_account and check_password_hash(service_account.password,
                    form.password.data):
                    token = create_session(service_account)
                    if token:
                        session['session_token'] = token
                        return redirect(url_for('users.home'))
                flash('Wrong email or password', 'error')
        return render_template("login.html", email_login_form=form)

class EmailLogin(WebView):

    def dispatch_request(self, *args, **kwargs):
        form = EmailLoginForm(request.form)
        if request.method == "POST":
            if form.validate_on_submit():
                service_account = get_service_account(name=form.email.data,
                    service=USER.LOCAL)
                if service_account and check_password_hash(service_account.password,
                    form.password.data):
                    token = create_session(service_account)
                    if token:
                        session['session_token'] = token
                        return redirect(url_for('users.home'))
                flash('Wrong email or password', 'error-message')
        return render_template("login_email.html", email_login_form=form)

class GenericOAuthLoginView(WebView):

    def __init__(self, service=None, oauth=None, oauth_handler=None, *args,
    **kwargs):
        super(GenericOAuthLoginView, self).__init__(*args, **kwargs)
        self.service = service
        self.oauth = oauth
        self.oauth_handler = oauth_handler

    def dispatch_request(self, *args, **kwargs):
        if g.service_account \
           and g.service_account.service != self.service and g.user is None:
            flash(USER.DENIED_MULTIPLE_ACCOUNTS, 'error')
            next_url = request.args.get('next') or url_for('users.login')
            return redirect(next_url)
        if g.service_account and g.service_account.service == self.service:
            flash(USER.ALREADY_LOGGED_IN, 'info')
            next_url = request.args.get('next') or url_for('users.home')
            return redirect(next_url)
        if g.user and self.service in [s.service for s in g.user.service_accounts]:
            def get_service_name(services):
                for service in services:
                    if self.service == service.service:
                        return service.name
                return None
            service_account = get_service_name(g.user.service_accounts)
            message = USER.ALREADY_ASSOCIATED % \
                      (USER.AUTH_SERVICE[self.service], service_account)
            flash(message, 'info')
            next_url = request.args.get('next') or url_for('users.home')
            return redirect(next_url)
        return self.oauth.authorize(callback=url_for(self.oauth_handler, _external=True))

class TwitterLoginOAuthHandler(WebView):

    def __init__(self, *args, **kwargs):
        super(TwitterLoginOAuthHandler, self).__init__(*args, **kwargs)
        oauth_login_handlers.append(self.__class__)

    @twitter.authorized_handler # TODO: prevent direct access
    def dispatch_request(self, *args, **kwargs):
        resp = kwargs['data']
        service_account = get_service_account(name=resp['screen_name'],
            service=USER.TWITTER)
        next_url = request.args.get('next') or url_for('users.login')

        if g.user:
            if service_account:
                connect_service_account_to_user(g.user, service_account)
            else:
                service_account = create_service_account(
                    name=resp['screen_name'],
                    oauth_token = resp['oauth_token'],
                    oauth_secret = resp['oauth_token_secret'],
                    service=USER.TWITTER
                )
                connect_service_account_to_user(g.user, service_account)
            session['session_token'] = create_session(service_account)
            flash(USER.ASSOCIATION_COMPLETE %
                  (USER.AUTH_SERVICE[USER.TWITTER], resp['screen_name']),
                'success')
            next_url = url_for('users.home')
        else:
            if service_account is not None:
                user = get_user(service_account=service_account)
                if user is not None:
                    session['session_token'] = create_session(service_account)
                    flash(u'Welcome %s %s' % (user.first_name, user.last_name))
                else:
                    session['session_token'] = create_session(service_account)
                    flash(u'Welcome back, %s. Please consider becoming a member.'
                          % service_account.name)
            else:
                service_account = create_service_account(
                    name=resp['screen_name'],
                    oauth_token = resp['oauth_token'],
                    oauth_secret = resp['oauth_token_secret'],
                    service=USER.TWITTER
                )
                session['session_token'] = create_session(service_account)
                flash(u'Your %s ID %s has been saved.' % (
                    USER.AUTH_SERVICE[USER.TWITTER], resp['screen_name']))
            if resp is None:
                flash(USER.LOGIN_DENIED)
        return redirect(next_url)

    @twitter.tokengetter
    def get_twitter_token(self):
        service_account = g.service_account
        if service_account is not None and \
           service_account.service == USER.TWITTER:
            return service_account.oauth_token, service_account.oauth_secret


class GoogleLoginOAuthHandler(WebView):

    def __init__(self, *args, **kwargs):
        super(GoogleLoginOAuthHandler, self).__init__(*args, **kwargs)
        oauth_login_handlers.append(self.__class__)

    @google.authorized_handler
    def dispatch_request(self, *args, **kwargs):
        resp = kwargs['data']
        access_token = resp['access_token']
        session['access_token'] = access_token, ''

        from urllib2 import Request, urlopen, URLError
        import json
        headers = {'Authorization': 'OAuth '+access_token}
        req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
            None, headers)
        try:
            res = urlopen(req)
        except URLError:
            return req.read() #TODO: Handle this

        data = json.loads(res.read())
        service_account = get_service_account(name=data['email'],
            service=USER.GOOGLE)
        next_url = request.args.get('next') or url_for('users.login')

        if g.user:
            if service_account:
                connect_service_account_to_user(g.user, service_account)
            else:
                service_account = create_service_account(
                    name=data['email'],
                    oauth_token = access_token,
                    service=USER.GOOGLE
                )
                connect_service_account_to_user(g.user, service_account)
            session['session_token'] = create_session(service_account)
            flash(USER.ASSOCIATION_COMPLETE %
                  (USER.AUTH_SERVICE[USER.GOOGLE], data['email']), 'success')
            next_url = url_for('users.home')
        else:
            if service_account is not None:
                user = get_user(service_account=service_account)
                if user is not None:
                    # create session
                    session['session_token'] = create_session(service_account)
                    flash(u'Welcome %s %s' % (user.first_name, user.last_name))
                else:
                    # Service account exists, but no user.
                    session['session_token'] = create_session(service_account)
                    flash(u'Welcome back, %s. Please consider becoming a member.'
                          % service_account.name)
            else:
                service_account = create_service_account(
                    name=data['email'],
                    oauth_token = access_token,
                    service=USER.GOOGLE
                )
                session['session_token'] = create_session(service_account)
                flash(u'Your %s ID %s has been saved.' % (
                    USER.AUTH_SERVICE[USER.GOOGLE], data['email']))
            if resp is None:
                flash(USER.LOGIN_DENIED)
        return redirect(next_url)

    @google.tokengetter
    def get_google_token(self):
        service_account = g.service_account
        if service_account is not None and \
           service_account.service == USER.GOOGLE:
            return service_account.oauth_token, service_account.oauth_secret

class FacebookLoginOAuthHandler(WebView):

    def __init__(self, *args, **kwargs):
        super(FacebookLoginOAuthHandler, self).__init__(*args, **kwargs)
        oauth_login_handlers.append(self.__class__)

    @facebook.authorized_handler
    def dispatch_request(self, *args, **kwargs):
        resp = kwargs['data']
        access_token = resp['access_token']
        session['access_token'] = access_token, ''
        from urllib2 import Request, urlopen, URLError
        import json
        req = Request('https://graph.facebook.com/me?access_token='+access_token)
        try:
            res = urlopen(req)
        except URLError:
            return req.read() #TODO: Handle this

        data = json.loads(res.read())

        service_account = get_service_account(name=data['username'],
            service=USER.FACEBOOK)
        next_url = request.args.get('next') or url_for('users.login')

        if g.user:
            if service_account:
                connect_service_account_to_user(g.user, service_account)
            else:
                service_account = create_service_account(
                    name=data['username'],
                    oauth_token = access_token,
                    service=USER.FACEBOOK
                )
                connect_service_account_to_user(g.user, service_account)
            session['session_token'] = create_session(service_account)
            flash(USER.ASSOCIATION_COMPLETE % (
                USER.AUTH_SERVICE[USER.FACEBOOK], data['username']), 'success')
            next_url = url_for('users.home')
        else:
            if service_account is not None:
                user = get_user(service_account=service_account)
                if user is not None:
                    session['session_token'] = create_session(service_account)
                    flash(u'Welcome %s %s' % (user.first_name, user.last_name))
                else:
                    # Service account exists, but no user.
                    session['session_token'] = create_session(service_account)
                    flash(u'Welcome back, %s. Please consider becoming a member.'
                          % service_account.name)
            else:
                service_account = create_service_account(
                    name=data['username'],
                    oauth_token = access_token,
                    service=USER.FACEBOOK
                )
                session['session_token'] = create_session(service_account)
                flash(u'Your %s ID %s has been saved.' % (
                    USER.AUTH_SERVICE[USER.FACEBOOK], data['username']))
        if resp is None:
            flash(USER.LOGIN_DENIED)
        return redirect(next_url)

    @facebook.tokengetter
    def get_facebook_token(self):
        service_account = g.service_account
        if service_account is not None and \
           service_account.service == USER.FACEBOOK:
            return service_account.oauth_token, service_account.oauth_secret


class Register(WebView):

    def dispatch_request(self, *args, **kwargs):
        form = RegisterForm(request.form)
        if request.method == "POST":
            if form.validate_on_submit():
                test_service_account = get_service_account(name=form.email.data)
                if test_service_account is not None:
                    service = USER.AUTH_SERVICE[test_service_account.service]
                    flash('This %s email address already exists. Please use it to log '
                          'in.' % service)
                    return redirect(url_for('users.login_email'))
                if not app.config['USER_REGISTRATION_REQUIRE_ACTIVATION']:
                    # require activation
                    status = USER.ACTIVE
                else:
                    status = USER.NEW
                user = create_user(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    phone=form.phone.data,
                    status=status)
                service_account = create_service_account(name=form.email.data,
                    password=generate_password_hash(form.password.data),
                    service=USER.LOCAL)
                if app.config['USER_REGISTRATION_EMAIL']:
                    # TODO: send an email
                    pass
                flash(USER.REGISTRATION_SUCCESSFUL, 'success')
                return redirect(url_for('users.login_email'))
            else:
                print "NOT VALIDATED"
                print form.errors
        return render_template(self.template_name, form=form)

# standard views
register_module_web_route(mod, Login, 'login', '/login/')
register_module_web_route(mod, WebView, 'help', '/help/',
    view_args={'template_name': "help.html"})
register_module_web_route(mod, Home, 'home', '/home/',
    view_args={'template_name': "home.html"})

# login and register pages
register_module_web_route(mod, EmailLogin, 'login_email', '/login/email/')
register_module_web_route(mod, GenericOAuthLoginView, 'login_twitter',
    '/login/twitter/',
    view_args = {'service': USER.TWITTER,
                 'oauth': twitter,
                 'oauth_handler': 'users.oauth_authorized_twitter'})
register_module_web_route(mod, GenericOAuthLoginView, 'login_google',
    '/login/google/',
    view_args = {'service': USER.GOOGLE,
                 'oauth': google,
                 'oauth_handler': 'users.oauth_authorized_google'})
register_module_web_route(mod, GenericOAuthLoginView, 'login_facebook',
    '/login/facebook/',
    view_args = {'service': USER.FACEBOOK,
                 'oauth': facebook,
                 'oauth_handler': 'users.oauth_authorized_facebook'})
register_module_web_route(mod, Register, 'register', '/register/',
    view_args={'template_name': "register.html"})

# OAuth handlers
register_module_web_route(mod, TwitterLoginOAuthHandler,
    'oauth_authorized_twitter', '/oauth-authorized/twitter/')
register_module_web_route(mod, GoogleLoginOAuthHandler,
    'oauth_authorized_google', '/oauth-authorized/google/')
register_module_web_route(mod, FacebookLoginOAuthHandler,
    'oauth_authorized_facebook', '/oauth-authorized/facebook/')

