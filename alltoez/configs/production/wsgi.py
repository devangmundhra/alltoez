import os
# put the Django project on sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alltoez.configs.production.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
