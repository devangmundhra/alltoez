from __future__ import absolute_import

__author__ = 'devangmundhra'

import logging

from django.conf import settings

from celery import shared_task
import predictionio

from apps.user_actions.models import View

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Get an instance of prediction io event client
pio_access_key = getattr(settings, 'PIO_ACCESS_KEY', "unknown access key")
pio_eventserver = getattr(settings, 'PIO_EVENT_SERVER_ENDPOINT', "http://localhost:7070")

@shared_task
def mark_user_views_event(event_id, user_id=None):
    view = View()
    view.event_id = event_id
    view.user_id = user_id
    view.save()

@shared_task
def pio_new_event(event_type, user_id, event_id, created):
    event_client = predictionio.EventClient(
        access_key=pio_access_key,
        url=pio_eventserver,
        threads=5, qsize=500)

    try:
        event_client.record_user_action_on_item(event_type, user_id, event_id,
                                                event_time=created)
    except predictionio.NotCreatedError:
        pass