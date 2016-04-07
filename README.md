# OAuth2
OAuth2 Web Application with account/application registration, account verification, [Authorization Code/Implicit/Password Credentials Grant](http://tools.ietf.org/html/rfc6749).

## Configuration
*   install the required tools python, pip, virtualenv
*	git clone https://github.com/twhtanghk/OAuth2.git
*   cd OAuth2
*   "pip install -r requirements.txt" to install required python library
*	update settings defined in 'organization/env.py'
```
SERVERURL = 'http://localhost:8000'

DEBUG = False    # set it to False for production environment and deploy static files on production environment accordingly

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

EMAIL_BACKEND = 'lib.backend.Notes'     # comment this setting to send mail by default smtp backend
DEFAULT_FROM_EMAIL = 'user@abc.com'     # default sender email address

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'https://mob.myvnc.com/org/users':  'Read User',
        'https://mob.myvnc.com/file':       'File',
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

## Web URL
* /:	user login, registration, forget password
* /users/me/: current login user profile, change password, delete account
* /oauth2/applications/: application CRUD
* /oauth2/authorize/: authorization URL

## Web API
* GET /api/users/me/: 
	*	in: authorization header "Authorization: Bearer TOKEN"
	*	out: json with user details or error for invalid token

* GET /api/oauth2/verify/:
	*	in: authorization header "Authorization: Bearer TOKEN"
	*	out: json with valid token details or error for invalid token
	
* POST /api/oauth2/token/:
	*	see script/oauth2.sh
	*	in: client id and secret, user id and secret, scope and url
	*	out: token in json e.g. {"access_token": "token", "token_type": "Bearer", "expires_in": 36000, "refresh_token": "refresh_token", "scope": "scope"}