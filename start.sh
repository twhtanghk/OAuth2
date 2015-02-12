#!/bin/bash

PORT=8000								# port to deploy the webapp
ROOT=~/prod/OAuth2						# web application root directory
VIRENV=~/virtualenv/dev/bin/activate	# python virtualenv script

cd ${ROOT}
source ${VIRENV}
./manage.py run_gunicorn -b 0.0.0.0:${PORT} >>stdout.out 2>&1