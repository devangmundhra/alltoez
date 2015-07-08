from __future__ import absolute_import

import logging
from datetime import datetime
from celery import shared_task

from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.models import Site

from apps.events.models import Event
from apps.events.eventparsers import redtri

# Get an instance of a logger
logger = logging.getLogger(__name__)

"""
Number of days before which an event for the date should be created
"""
EVENTS_NUM_DAYS_SCRAPE_LOOK_AHEAD = 11


@shared_task
def scrape_events_look_ahead():
    """
    Scraping of websites for kids events
    :return:
    """
    get_redtri_events()
    get_expired_events()


def get_redtri_events():
    today = datetime.today()

    try:
        redtri_events = redtri.get_events(EVENTS_NUM_DAYS_SCRAPE_LOOK_AHEAD)
        redtri_events_context = []
        for parsed_event in redtri_events:
            title = parsed_event.get('title', None)
            url = parsed_event.get('orig_link', None)
            redtri_events_context.append({"event_url": url, "event_title": title})
        if redtri_events_context and not settings.DEBUG:
            # Now send mail
            subject = "Alltoez | Redtri events | {}".format(today.strftime("%A, %d. %B"))

            msg = EmailMessage(subject=subject, from_email=("No Reply", "noreply@alltoez.com"),
                               to=["devangmundhra@gmail.com", "ruchikadamani90@gmail.com"])
            msg.template_name = "RedTri Events"
            msg.global_merge_vars = {
                "events": redtri_events_context,
                "CHECK_DATE": "{}".format(today.strftime("%A, %d. %B")),
                "redtri_event_count": len(redtri_events_context)
            }
            msg.send()

    except Exception:
        pass


def get_expired_events():
    today = datetime.today()
    expired_events_qs = Event.objects.filter(end_date=datetime.today())
    if expired_events_qs:
        expired_events = []
        for event in expired_events_qs:
            expired_events.append({"event_url": "http://" + Site.objects.get_current().domain + event.get_absolute_url(),
                                   "event_title": event.title, "image_url": event.image.url})

        if not settings.DEBUG:
            # Now send mail
            subject = "Alltoez | Expired Events | {}".format(today.strftime("%A, %d. %B"))

            msg = EmailMessage(subject=subject, from_email=("No Reply", "noreply@alltoez.com"),
                               to=["devangmundhra@gmail.com", "ruchikadamani90@gmail.com"])
            msg.template_name = "Expired Events"
            msg.global_merge_vars = {
                "events": expired_events,
                "CHECK_DATE": "{}".format(today.strftime("%A, %d. %B")),
                "expired_count": expired_events_qs.count()
            }
            msg.send()
