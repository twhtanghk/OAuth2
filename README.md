# OAuth2
OAuth2 Web Application with account/application registration, account verification, [Authorization Code/Implicit/Password Credentials Grant](http://tools.ietf.org/html/rfc6749).

## Configuration
* update environment variables defined in .env
* docker-compose -f docker-compose.yml up -d
* create mysql database (e.g. org) and create database user with appropriate access right
* create tables with pre-defined schema 
```
manage.py syncdb
```
* update domain defined in the created site table
```
update django_site set domain='domain here', name='domain here';
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

* GET /oauth2/verify/:
	*	in: authorization header "Authorization: Bearer TOKEN"
	*	out: json with valid token details or error for invalid token
	
* POST /oauth2/token/:
	*	see script/oauth2.sh
	*	in: client id and secret, user id and secret, scope and url
	*	out: token in json e.g. {"access_token": "token", "token_type": "Bearer", "expires_in": 36000, "refresh_token": "refresh_token", "scope": "scope"}
	
## Housekeeping to clear expired tokens
* python manage.py cleartokens
