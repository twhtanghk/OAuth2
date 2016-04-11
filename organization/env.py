import os

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

ROOT_URLCONF = 'organization.urls'

SERVERURL = 'http://localhost:8000'
FORCE_SCRIPT_NAME = '/org'

LOGIN_REDIRECT_URL = 'accounts/profile/'
LOGIN_URL = 'accounts/login/'
LOGOUT_URL = 'accounts/logout/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = os.path.join(SERVERURL, FORCE_SCRIPT_NAME, "static/")

DEBUG = False    # set it to False for production environment and deploy static files on production environment accordingly

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'org',  # Or path to database file if using sqlite3.
        'USER': 'root',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'errorlog': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/error.log',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['errorlog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        
    }
}

REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size' 
}

# email setting
EMAIL_BACKEND = 'lib.backend.Notes'     # comment this setting to send mail by default smtp backend
DEFAULT_FROM_EMAIL = 'user@abc.com'     # default sender email address
# web service
EMAIL_HOST = 'http://localhost:8001/mail/api/mail/' 
# gmail
"""
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "user@gmail.com"
EMAIL_HOST_PASSWORD = "password here"
"""
# abc.com
"""
EMAIL_HOST = 'smtpa.abc.com' 
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "user@abc.com"
EMAIL_HOST_PASSWORD = "password here"
"""

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''
SOCIAL_AUTH_YAHOO_OAUTH_KEY = ''
SOCIAL_AUTH_YAHOO_OAUTH_SECRET = ''
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'https://mob.myvnc.com/org/users':  'User',
        'https://mob.myvnc.com/file':       'File',
        'https://mob.myvnc.com/xmpp':       'XMPP',
        'https://mob.myvnc.com/todo':       'Todo',
        'https://mob.myvnc.com/mobile':     'Mobile'
    }
}