from __future__ import absolute_import

__author__ = 'devangmundhra'

import logging

from celery import shared_task

from apps.user_actions.models import View

# Get an instance of a logger
logger = logging.getLogger(__name__)

@shared_task
def mark_user_views_event(event_id, user_id=None):
    view = View()
    view.event_id = event_id
    view.user_id = user_id
    view.save()