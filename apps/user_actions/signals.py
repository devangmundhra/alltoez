__author__ = 'devangmundhra'

import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.user_actions.models import Bookmark, Done, View, Review
from apps.user_actions.tasks import new_action, bookmark_post_delete_task, bookmark_post_save_task
from apps.user_actions.tasks import done_post_delete_task, done_post_save_task


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
    done_post_save_task.delay(user_action.id)


@receiver(post_save, sender=Bookmark)
def bookmark_post_save(sender, **kwargs):
    user_action = kwargs.get('instance')
    new_action.delay(sender._meta.object_name, user_action.user.id, user_action.event.id)
    bookmark_post_save_task.delay(user_action.id)


@receiver(post_delete, sender=Bookmark)
def bookmark_post_delete(sender, instance, **kwargs):
    bookmark_post_delete_task.delay(instance.event.id, instance.user.id)


## POST_DELETES
@receiver(post_delete, sender=Done)
def done_post_delete(sender, instance, **kwargs):
    done_post_delete_task.delay(instance.event.id, instance.user.id)