alltoez
=======

Repository for Django project for Alltoez

To setup development environment:
- Clone the project
- Install dependencies by "pip install -r requirements.txt"
- Make sure Postgres is running and create a database named alltoez_dev
- Run "python manage.py syncdb"
- Start Redis and run "celery -A alltoez worker -l info -B" (-B option is for celerybeat)
- Run "python manage.py runserver"

To run tests:
- python manage.py test