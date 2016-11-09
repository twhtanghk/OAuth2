import os

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

ROOT_URLCONF = 'organization.urls'

SERVERURL = os.environ['URL']
FORCE_SCRIPT_NAME = os.environ['PREFIX']

LOGIN_REDIRECT_URL = 'accounts/profile/'
LOGIN_URL = 'accounts/login/'
LOGOUT_URL = 'accounts/logout/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = os.path.join(SERVERURL, FORCE_SCRIPT_NAME, "static/")

DEBUG = False    # set it to False for production environment and deploy static files on production environment accordingly

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [os.environ['SERVER'], 'localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ['DBNAME'],  # Or path to database file if using sqlite3.
        'USER': os.environ['DBUSER'],  # Not used with sqlite3.
        'PASSWORD': os.environ['DBPASS'],  # Not used with sqlite3.
        'HOST': os.environ['DBHOST'],  # Set to empty string for localhost. Not used with sqlite3.
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
#EMAIL_BACKEND = 'lib.backend.Notes'     # comment this setting to send mail by default smtp backend
DEFAULT_FROM_EMAIL = os.environ['EMAILUSER']     # default sender email address
# web service
EMAIL_HOST = 'http://localhost:8001/mail/api/mail/' 
EMAIL_HOST = os.environ['EMAILHOST']
EMAIL_PORT = int(os.environ['EMAILPORT'])
EMAIL_USE_TLS = os.environ['EMAILTLS'] == 'True'
EMAIL_HOST_USER = os.environ['EMAILUSER']
EMAIL_HOST_PASSWORD = os.environ['EMAILPASS']

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
        'User':  'User',
        'Mobile': 'Mobile'
    }
}
