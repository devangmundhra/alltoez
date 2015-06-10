from __future__ import absolute_import

import logging
from datetime import datetime
from celery import shared_task

from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

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
            redtri_events_context.append({"url": url, "title": title})
        if redtri_events_context and not settings.DEBUG:
            # Now send mail
            plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
            subject = "Alltoez | Redtri events | {}".format(today.strftime("%A, %d. %B"))
            text_body = render_to_string("email/redtri_scrape/redtri_scrape.txt",
                                         {"redtri_events": redtri_events_context}, plaintext_context)
            html_body = render_to_string("email/redtri_scrape/redtri_scrape.html",
                                         {"redtri_events": redtri_events_context, "site": Site.objects.get_current()})

            msg = EmailMultiAlternatives(subject=subject, from_email=("No Reply", "noreply@alltoez.com"),
                                         to=["devangmundhra@gmail.com", "ruchikadamani90@gmail.com"], body=text_body)
            msg.attach_alternative(html_body, "text/html")
            msg.send()
    except Exception:
        pass


def get_expired_events():
    today = datetime.today()
    expired_events_qs = Event.objects.filter(end_date=datetime.today())
    if expired_events_qs:
        expired_events = []
        for event in expired_events_qs:
            expired_events.append({"url": event.url, "title": event.title})

        if not settings.DEBUG:
            # Now send mail
            plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
            subject = "Alltoez | Expired Events | {}".format(today.strftime("%A, %d. %B"))
            text_body = render_to_string("email/expired_events/expired_events.txt",
                                         {"expired_events": expired_events}, plaintext_context)
            html_body = render_to_string("email/expired_events/expired_events.html",
                                         {"expired_events": expired_events, "site": Site.objects.get_current()})

            msg = EmailMultiAlternatives(subject=subject, from_email="noreply@alltoez.com",
                                         to=["devangmundhra@gmail.com", "ruchikadamani90@gmail.com"], body=text_body)
            msg.attach_alternative(html_body, "text/html")
            msg.send()
