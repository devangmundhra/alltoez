__author__ = 'devangmundhra'

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.venues.models import Venue

# Get an instance of a logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Venue)
def venue_post_save(sender, **kwargs):
    pass