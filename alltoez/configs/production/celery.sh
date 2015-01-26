#!/bin/bash
set -e
LOGFILE=/home/django/logs/worker.log
ERRORFILE=/home/django/logs/worker.log
LOGDIR=$(dirname $LOGFILE)

NEW_RELIC_CONFIG_FILE=/home/django/sites/alltoez/repository/alltoez/configs/production/newrelic.ini
export NEW_RELIC_CONFIG_FILE
NEW_RELIC_ENVIRONMENT=production
export NEW_RELIC_ENVIRONMENT

cd /home/django/sites/alltoez/repository
source ../env/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/django/sites/alltoez/repository/alltoez
cd /home/django/sites/alltoez/repository/alltoez/configs/production
test -d $LOGDIR || mkdir -p $LOGDIR
newrelic-admin run-program /home/django/sites/alltoez/env/bin/celery worker -A celeryapp --loglevel=INFO
