#!/bin/bash
set -e
  LOGFILE=/var/log/gunicorn/pegapega.log
  NUM_WORKERS=9
  # user/group to run as
  USER=web
  GROUP=web
  cd /var/www/pegapega
  source ./bin/activate
  # NEW_RELIC_CONFIG_FILE=newrelic.ini
  # export NEW_RELIC_CONFIG_FILE
  # exec newrelic-admin run-program gunicorn_django -w $NUM_WORKERS \
  exec gunicorn -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=error \
    --log-file=$LOGFILE 2>>$LOGFILE pegapega.wsgi:application
