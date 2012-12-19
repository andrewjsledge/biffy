__author__ = 'andrew'

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

ADMINS = frozenset(['youremail@yourdomain.com'])
SECRET_KEY = 'SecretKeyForSessionSigning'
DEBUG_TB_PROFILER_ENABLED=True
DEBUG_TB_INTERCEPT_REDIRECTS=False

###
# Permanent storage
###
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
    _basedir, 'application.db'
)
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_ECHO = DEBUG

###
# Caching
###
CACHE_TANK = "simple"

if CACHE_TANK == "memcached":
    from werkzeug.contrib.cache import MemcachedCache
    cache = MemcachedCache(['127.0.0.1:11211'])
elif CACHE_TANK == "simple" or CACHE_TANK == "" or CACHE_TANK is None:
    from werkzeug.contrib.cache import SimpleCache
    cache = SimpleCache()

THREADS_PER_PAGE = 8

CSRF_ENABLED=True
CSRF_SESSION_KEY="somethingimpossibletoguess"

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = 'blahblahblahblahblahblahblahblahblah'
RECAPTCHA_PRIVATE_KEY = 'blahblahblahblahblahblahprivate'
RECAPTCHA_OPTIONS = {'theme': 'white'}