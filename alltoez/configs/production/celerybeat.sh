#!/bin/bash
set -e
LOGFILE=/home/django/logs/beat.log
ERRORFILE=/home/django/logs/beat.log
LOGDIR=$(dirname $LOGFILE)
PIDFILE=/home/celery/celerybeat.pidfile
PIDDIR=$(dirname $PIDFILE)
SCHEDFILE=/home/celery/celerybeat_sched
SCHEDDIR=$(dirname $SCHEDFILE)

NEW_RELIC_CONFIG_FILE=/home/django/sites/alltoez/repository/alltoez/configs/production/newrelic.ini
export NEW_RELIC_CONFIG_FILE
NEW_RELIC_ENVIRONMENT=production
export NEW_RELIC_ENVIRONMENT

cd /home/django/sites/alltoez/repository
source ../env/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/django/sites/alltoez/repository/alltoez
cd /home/django/sites/alltoez/repository/alltoez/configs/production
test -d $LOGDIR || mkdir -p $LOGDIR
test -d $PIDDIR || mkdir -p $PIDDIR
test -d $SCHEDDIR || mkdir -p $SCHEDDIR
newrelic-admin run-program /home/django/sites/alltoez/env/bin/celery beat -A celeryapp --loglevel=INFO --pidfile=$PIDFILE --schedule=$SCHEDFILE
