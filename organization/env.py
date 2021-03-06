import os

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

ROOT_URLCONF = 'organization.urls'

SERVERURL = os.environ['URL']
FORCE_SCRIPT_NAME = os.environ['PREFIX']

LOGIN_REDIRECT_URL = FORCE_SCRIPT_NAME + '/accounts/profile/'
LOGIN_URL = FORCE_SCRIPT_NAME + '/accounts/login/'
LOGOUT_URL = FORCE_SCRIPT_NAME + '/accounts/logout/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = os.path.join(SERVERURL, FORCE_SCRIPT_NAME, "static/")

DEBUG = False   # set it to False for production environment and deploy static files on production environment accordingly

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
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
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
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['errorlog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'organization': {
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

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'User':  'User',
        'Mobile': 'Mobile'
    }
}
