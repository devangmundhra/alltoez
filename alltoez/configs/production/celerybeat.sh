#!/bin/bash
set -e
LOGFILE=/home/django/logs/beat.log
ERRORFILE=/home/django/logs/beat.log
LOGDIR=$(dirname $LOGFILE)

#we don't want to run this as root..
USER=www-data
GROUP=www-data

cd /home/django/sites/alltoez/repository
source ../env/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/django/sites/alltoez/repository/alltoez
cd /home/django/sites/alltoez/repository/alltoez/configs/production
test -d $LOGDIR || mkdir -p $LOGDIR
exec /home/django/sites/alltoez/env/bin/celery beat -A celeryapp --schedule /var/lib/celery/beat.db --loglevel=INFO
