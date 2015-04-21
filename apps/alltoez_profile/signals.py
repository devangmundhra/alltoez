__author__ = 'devangmundhra'

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.alltoez_profile.models import UserProfile

# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(post_save, sender=UserProfile)
def userprofile_post_save(sender, **kwargs):
    pass
