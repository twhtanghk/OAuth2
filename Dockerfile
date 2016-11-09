FROM python:2

WORKDIR /usr/src/app
ADD https://github.com/twhtanghk/OAuth2/archive/master.tar.gz /tmp
RUN tar --strip-components=1 -xzf /tmp/master.tar.gz && \
	pip install -r requirements.txt && \
	rm /tmp/master.tar.gz
EXPOSE 8000	
ENTRYPOINT ./manage.py runserver 0.0.0.0:8000
