from flask import Blueprint
from application.users.utils import BiffyOAuth

mod = Blueprint('users', __name__, url_prefix='/users',
    template_folder='templates', static_folder='static')

oauth = BiffyOAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='4VChcqumAvPK7jk5NfjAQ',
    consumer_secret='SGa7qmfo12lKgEoYWqVnC6PJpfSKDHdnHaSeJ1NoE'
)

google = oauth.remote_app('google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key="873141028602.apps.googleusercontent.com",
    consumer_secret="qXY1rkLGz2NVKjhqiIfk33nC",
)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key="180670042069972",
    consumer_secret="f429551b068a444a17600eb077b01922",
    request_token_params={'scope': 'email'}
)