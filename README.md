Repository for Django project for Alltoez

To setup development environment:

Clone the project
Install dependencies by "pip install -r requirements.txt"
MUST RUN sudo npm install -g less
Make sure Postgres is running and create a database named alltoez_dev
Run "python manage.py syncdb"
Start Redis and run "celery -A alltoez worker -l info -B" (-B option is for celerybeat)
Run "python manage.py runserver"
To run tests:

python manage.py test

If syncdb fails due to GEOSException error, postgis installation might be needed.
For Ubuntu, check http://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS21UbuntuPGSQL93Apt
For Mac/Windows, https://docs.djangoproject.com/en/1.6/ref/contrib/gis/install/#macosx
