#!/bin/bash
set -e
LOGFILE=/home/django/logs/beat.log
ERRORFILE=/home/django/logs/beat.log
LOGDIR=$(dirname $LOGFILE)
PIDFILE=/home/celery/celery.pidfile
PIDDIR=$(dirname $PIDFILE)
SCHEDFILE=/home/celery/celerybeat_sched
SCHEDDIR=$(dirname $SCHEDFILE)

#we don't want to run this as root..
#USER=celery
#GROUP=celery

cd /home/django/sites/alltoez/repository
source ../env/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/django/sites/alltoez/repository/alltoez
cd /home/django/sites/alltoez/repository/alltoez/configs/production
test -d $LOGDIR || mkdir -p $LOGDIR
#test -d $PIDDIR || mkdir -p $PIDDIR
#sudo chown $USER:$GROUP $PIDDIR
#test -d SCHEDDIR || mkdir -p SCHEDDIR
#sudo chown $USER:$GROUP SCHEDDIR
exec /home/django/sites/alltoez/env/bin/celery beat -A celeryapp --loglevel=INFO #--pidfile=$PIDFILE --schedule=$SCHEDFILE
