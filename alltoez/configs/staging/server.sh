#!/bin/bash
set -e
LOGFILE=/home/rawjam/logs/alltoez_gunicorn.access.log
ERRORFILE=/home/rawjam/logs/alltoez_gunicorn.error.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3  #recommended formula here is 1 + 2 * NUM_CORES

ADDRESS=unix:/var/run/alltoez.sock

cd /home/rawjam/sites/alltoez/repository
source ../env/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/rawjam/sites/alltoez/repository/rawjam
export PYTHONPATH=$PYTHONPATH:/home/rawjam/sites/alltoez/repository/alltoez
test -d $LOGDIR || mkdir -p $LOGDIR
exec ../env/bin/gunicorn_django -w $NUM_WORKERS --bind=$ADDRESS \
	--log-level=debug \
	--log-file=$LOGFILE 2>>$LOGFILE  1>>$ERRORFILE \
	--settings=alltoez.configs.staging.settings
