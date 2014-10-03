#!/bin/bash
set -e
LOGFILE=/home/django/logs/alltoez_gunicorn.access.log
ERRORFILE=/home/django/logs/alltoez_gunicorn.error.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3  #recommended formula here is 1 + 2 * NUM_CORES

#we don't want to run this as root..
USER=www-data
GROUP=www-data

cd /home/django/sites/alltoez/repository
source ../env/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/django/sites/alltoez/repository/rawjam
export PYTHONPATH=$PYTHONPATH:/home/django/sites/alltoez/repository/alltoez
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn_django -w $NUM_WORKERS \
	--log-level=debug \
	--log-file=$LOGFILE 2>>$LOGFILE  1>>$ERRORFILE \
	--settings=alltoez.configs.production.settings \
	--user=$USER --group=$GROUP
