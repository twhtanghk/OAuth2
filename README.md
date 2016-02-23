# OAuth2
OAuth2 Web Application with account/application registration, account verification, [Authorization Code/Implicit/Password Credentials Grant](http://tools.ietf.org/html/rfc6749).

## Configuration
*   install the required tools python, pip, virtualenv
*	git clone https://github.com/twhtanghk/OAuth2.git
*   cd OAuth2
*   "pip install -r requirements.txt" to install required python library
*	update settings defined in 'organization/env.py'
```
ROOTAPP = 'org'     # deployed context path of the web app

SERVERURL = 'http://localhost:8000'

DEBUG = True    # set it to False for production environment and deploy static files on production environment accordingly

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'org',  # Or path to database file if using sqlite3.
        'USER': 'orgrw',  # Not used with sqlite3.
        'PASSWORD': 'password here',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

EMAIL_BACKEND = 'lib.backend.Notes'     # comment this setting to send mail by default smtp backend
DEFAULT_FROM_EMAIL = 'user@abc.com'     # default sender email address

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
        'https://mob.myvnc.com/org/users':  'Read User',
        'https://mob.myvnc.com/file':       'File',
        'https://mob.myvnc.com/xmpp':       'XMPP',
        'https://mob.myvnc.com/todo':       'Todo',
        'https://mob.myvnc.com/mobile':     'Mobile'
    }
}
```
*	create database 'org' on mysql and create database user with appropriate access right
*	create tables for Web Application schema
```
manage.py syncdb
```
*	update domain defined in the created site table
```
update django_site set domain='domain here' and name='domain here';
``` 
*	update environment variables in start.sh

```
PORT=8000								# port to deploy the webapp
ROOT=~/prod/OAuth2						# web application root directory
VIRENV=~/virtualenv/dev/bin/activate	# python virtualenv script
```
*	run 'start.sh' to start the web application

## Web URL
* /org:	user login, registration, forget password
* /org/users/me/: current login user profile, change password, delete account
* /org/developers/applications:	application CRUD
* /org/oauth2/authorize/: authorization URL

## Web API
* GET /org/api/users/me/: 
	*	in: authorization header "Authorization: Bearer TOKEN"
	*	out: json with user details or error for invalid token

* GET /org/api/oauth2/verify/:
	*	in: authorization header "Authorization: Bearer TOKEN"
	*	out: json with valid token details or error for invalid token
	
* POST /org/api/oauth2/token/:
	*	see script/oauth2.sh
	*	in: client id and secret, user id and secret, scope and url
	*	out: token in json e.g. {"access_token": "token", "token_type": "Bearer", "expires_in": 36000, "refresh_token": "refresh_token", "scope": "scope"}