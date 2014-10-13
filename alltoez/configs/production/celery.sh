#!/bin/bash
set -e
LOGFILE=/home/django/logs/worker.log
ERRORFILE=/home/django/logs/worker.log
LOGDIR=$(dirname $LOGFILE)

cd /home/django/sites/alltoez/repository
source ../env/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/django/sites/alltoez/repository/alltoez
cd /home/django/sites/alltoez/repository/alltoez/configs/production
test -d $LOGDIR || mkdir -p $LOGDIR
exec /home/django/sites/alltoez/env/bin/celery worker -A celeryapp --loglevel=INFO
