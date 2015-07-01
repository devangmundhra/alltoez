__author__ = 'devangmundhra'

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.events.models import Event, Category

# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Event)
def event_post_save(sender, instance, created, **kwargs):
    instance.create_graph_node()


@receiver(post_save, sender=Category)
def category_post_save(sender, instance, created, **kwargs):
    instance.create_graph_node()