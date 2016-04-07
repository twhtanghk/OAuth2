FROM python:2

WORKDIR /usr/src/app
ADD https://github.com/twhtanghk/server.dns/archive/master.tar.gz /tmp
RUN tar --strip-components=1 -xzf /tmp/master.tar.gz && \
	pip install -r requirements.txt && \
	rm /tmp/master.tar.gz
	
ENTRYPOINT python manage.py runserver 0.0.0.0:8000