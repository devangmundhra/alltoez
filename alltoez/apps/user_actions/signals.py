__author__ = 'devangmundhra'

import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

import predictionio

from apps.user_actions.models import Bookmark, Done, View
# Get an instance of a logger
logger = logging.getLogger(__name__)

# Get an instance of prediction io event client
pio_access_key = getattr(settings, 'PIO_ACCESS_KEY', None)
pio_eventserver = getattr(settings, 'PIO_EVENT_SERVER_ENDPOINT', None)

event_client = predictionio.EventClient(
    access_key=pio_access_key,
    url=pio_eventserver,
    threads=5, qsize=500)


def pio_new_event(event_type, user_action):
    try:
        event_client.record_user_action_on_item(event_type, user_action.user.id, user_action.event.id,
                                                event_time=user_action.created)
    except predictionio.NotCreatedError:
        pass


@receiver(post_save, sender=View)
def view_post_save(sender, **kwargs):
    user_action = kwargs.get('instance')
    pio_new_event('view', user_action)


@receiver(post_save, sender=Done)
def done_post_save(sender, **kwargs):
    user_action = kwargs.get('instance')
    pio_new_event('done', user_action)


@receiver(post_save, sender=Bookmark)
def bookmark_post_save(sender, **kwargs):
    user_action = kwargs.get('instance')
    pio_new_event('bookmark', user_action)


@receiver(post_delete, sender=Bookmark)
def bookmark_post_delete(sender, **kwargs):
    # TODO: Need to create a table to map this id to event_id returned by pio event server
    pass
