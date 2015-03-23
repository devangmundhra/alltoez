web: newrelic-admin gunicorn alltoez.wsgi --log-file -
worker: newrelic-admin run-program celery -A alltoez worker -l info -B
