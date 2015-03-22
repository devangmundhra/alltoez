import os, sys
# put the Django project on sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alltoez.settings")

# Appending the path instead of inserting since there are some module (like celery)
# which we would like Django to pick up from the absolute_path (not the project path)
ROOT = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(ROOT)
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(PROJECT_ROOT)

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())