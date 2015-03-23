web: newrelic-admin run-program gunicorn alltoez.wsgi --log-file -
worker: newrelic-admin run-program celery -A alltoez worker -l info -B
