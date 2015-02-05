#!/bin/bash
set -e
LOGFILE=/home/django/logs/alltoez_gunicorn.access.log
ERRORFILE=/home/django/logs/alltoez_gunicorn.error.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3  #recommended formula here is 1 + 2 * NUM_CORES

#we don't want to run this as root..
USER=www-data
GROUP=www-data

NEW_RELIC_CONFIG_FILE=/home/django/sites/alltoez/repository/alltoez/configs/production/newrelic.ini
export NEW_RELIC_CONFIG_FILE
NEW_RELIC_ENVIRONMENT=production
export NEW_RELIC_ENVIRONMENT

cd /home/django/sites/alltoez/repository
source ../env/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/django/sites/alltoez/repository/alltoez
test -d $LOGDIR || mkdir -p $LOGDIR
newrelic-admin run-program gunicorn -w $NUM_WORKERS \
	--log-level debug \
	--access-logfile $LOGFILE \
	--log-file $ERRORFILE \
	--env DJANGO_SETTINGS_MODULE=alltoez.configs.production.settings \
	--user $USER --group $GROUP alltoez.configs.production.wsgi \
	--max_requests 1000
