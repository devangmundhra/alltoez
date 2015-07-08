__author__ = 'devangmundhra'

import logging
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site

from celery import shared_task

from apps.events.models import Event, SimilarEvents
from apps.alltoez_profile.models import UserProfile
from apps.user_actions.models import Bookmark
from apps.alltoez.ml.pio_data import get_similar_events

# Get an instance of a logger
logger = logging.getLogger(__name__)


@shared_task
def update_similar_events_mapping():
    for event in Event.objects.filter(publish=True).filter(Q(end_date__gte=timezone.now().date()) | Q(end_date=None)):
        similar_event_ids = get_similar_events(event)
        se, created = SimilarEvents.objects.get_or_create(event=event)
        if similar_event_ids:
            se.similar_events = Event.objects.filter(pk__in=similar_event_ids)
            se.save()


@shared_task
def send_bookmark_reminder_email():
    for profile in UserProfile.objects.all():
        user = profile.user
        # Get all bookmarked events ending in the next 7 days from today
        # What day will it be 7 days from now-
        now = timezone.now().date()
        seven_days = now + timedelta(days=7)
        my_bookmarks = Bookmark.objects.filter(user=user, event__end_date__lte=seven_days)

        if my_bookmarks:
            bookmarked_events = []

            for bookmark in my_bookmarks:
                bookmarked_events.append({"EVENT_TITLE": bookmark.event.title,
                                     "IMAGE_URL": bookmark.event.image.url,
                                     "EVENT_DESCRIPTION": bookmark.event.description,
                                     "EVENT_URL": "http://" + Site.objects.get_current().domain + bookmark.event.get_absolute_url(),
                                     "END_DATE": "{}".format(bookmark.event.end_date.strftime("%A, %d. %B"))})
            subject = "Events ending soon on Alltoez"

            msg = EmailMessage(subject=subject, from_email=("Alltoez", "hi@alltoez.com"),
                               to=[user.email])
            msg.template_name = "Bookmarked Events Ending"
            msg.global_merge_vars = {
                "USER_NAME": profile.first_name,
                "events": bookmarked_events,
            }
            msg.send()