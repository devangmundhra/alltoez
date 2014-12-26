import os, sys

# put the Django project on sys.path
sys.path.insert(0, '/home/alltoez/sites/alltoez/repository')
sys.path.insert(0, '/home/alltoez/sites/alltoez/repository/allauth')
sys.path.insert(0, '/home/alltoez/sites/alltoez/repository/alltoez')

os.environ["DJANGO_SETTINGS_MODULE"] = "alltoez.configs.staging.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()