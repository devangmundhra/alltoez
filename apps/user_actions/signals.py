__author__ = 'devangmundhra'

import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.user_actions.models import Bookmark, Done, View
from apps.user_actions.tasks import pio_new_event
# Get an instance of a logger
logger = logging.getLogger(__name__)

## POST_SAVES
@receiver(post_save, sender=View)
def view_post_save(sender, **kwargs):
    user_action = kwargs.get('instance')
    pio_new_event('view', user_action.user.id, user_action.event.id, user_action.created)


@receiver(post_save, sender=Done)
def done_post_save(sender, **kwargs):
    user_action = kwargs.get('instance')
    pio_new_event('done', user_action.user.id, user_action.event.id, user_action.created)

@receiver(post_save, sender=Bookmark)
def bookmark_post_save(sender, **kwargs):
    user_action = kwargs.get('instance')
    pio_new_event('bookmark', user_action.user.id, user_action.event.id, user_action.created)


@receiver(post_delete, sender=Bookmark)
def bookmark_post_delete(sender, **kwargs):
    # TODO: Need to create a table to map this id to event_id returned by pio event server
    pass

## POST_DELETES
@receiver(post_delete, sender=Done)
def done_post_delete(sender, **kwargs):
    pass