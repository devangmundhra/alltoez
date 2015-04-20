__author__ = 'devangmundhra'

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from cacheops import invalidate_obj, invalidate_model

from apps.venues.models import Venue

# Get an instance of a logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Venue)
def venue_post_save(sender, **kwargs):
    return
    venue = kwargs['instance']
    events = venue.events
    for event in events:
        invalidate_obj(event)