__author__ = 'devangmundhra'

import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.user_actions.models import Bookmark, Done, View, Review
from apps.user_actions.tasks import new_action
# Get an instance of a logger
logger = logging.getLogger(__name__)

## POST_SAVES
@receiver(post_save, sender=View)
def view_post_save(sender, **kwargs):
    user_action = kwargs.get('instance')
    new_action.delay(sender._meta.object_name, user_action.user.id, user_action.event.id)


@receiver(post_save, sender=Done)
def done_post_save(sender, **kwargs):
    user_action = kwargs.get('instance')
    new_action.delay(sender._meta.object_name, user_action.user.id, user_action.event.id)

@receiver(post_save, sender=Bookmark)
def bookmark_post_save(sender, **kwargs):
    user_action = kwargs.get('instance')
    new_action.delay(sender._meta.object_name, user_action.user.id, user_action.event.id)


@receiver(post_delete, sender=Bookmark)
def bookmark_post_delete(sender, **kwargs):
    # TODO: Need to create a table to map this id to event_id returned by pio event server
    pass

## POST_DELETES
@receiver(post_delete, sender=Done)
def done_post_delete(sender, **kwargs):
    done = kwargs.get('instance')
    try:
        review = Review.objects.get(user=done.user, event=done.event)
        review.delete()
    except Review.DoesNotExist:
        pass