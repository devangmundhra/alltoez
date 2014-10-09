from __future__ import absolute_import

import os, sys

from celery import Celery

from django.conf import settings

python_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../../../'
)
# we have have a local apps directory
apps_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../../'
)

allauth_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../../../allauth'
)

# we add them first to avoid any collisions
sys.path.insert(0, python_path)
sys.path.insert(0, apps_path)
sys.path.insert(0, allauth_path)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
app = Celery('common')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
