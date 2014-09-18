# -*- coding: utf-8 -*-
from __future__ import absolute_import

__about__ = """
This project is similar to pinax-project-account in providing a foundation for
sites that have user accounts but it differs in supporting social
authentication rather than local password based authentication.
"""

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app