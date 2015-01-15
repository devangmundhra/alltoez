from __future__ import absolute_import

import logging
from datetime import datetime, timedelta
from croniter import croniter
from celery import shared_task

from django.utils import timezone
from django.core.mail import send_mail

from apps.events.models import Event, EventRecord
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
    today = datetime.today()
    event_date = today + timedelta(days=EVENTS_NUM_DAYS_SCRAPE_LOOK_AHEAD)

    subject = "Alltoez Events Summary | {}".format(today.strftime("%A, %d. %B"))
    body = "For date {}\n\n".format(event_date.strftime("%A, %d. %B %Y")) + get_redtri_events_body() \
           + get_expired_events_body

    send_mail(subject, body, "noreply@alltoez.com", ["ruchikadamani90@gmail.com", "devangmundhra@gmail.com"])


def get_redtri_events_body():
    body = "\n"

    try:
        redtri_events = redtri.get_events(EVENTS_NUM_DAYS_SCRAPE_LOOK_AHEAD)
        body = body + "{} RedTri Events\n".format(len(redtri_events), )
        for parsed_event in redtri_events:
            title = parsed_event.get('title', None)
            url = parsed_event.get('orig_link', None)
            body = body + "<a href={}>{}</a>\n".format(url.encode('ascii', 'ignore'), title.encode('ascii', 'ignore'))
    except:
        pass

    return body


def get_expired_events_body():
    body = "\n"

    expired_events = Event.objects.filter(end_date=datetime.today())
    if expired_events:
        body = body + "{} Expired Events\n".format(len(expired_events), )
    for event in expired_events:
        body = body + "<a href={}>{}</a>\n".format(event.url.encode('ascii', 'ignore'),
                                                   event.title.encode('ascii', 'ignore'))

    return body

"""
Number of days before which an event for the date should be created
"""
EVENTS_NUM_DAYS_RECORD_LOOK_AHEAD = 8


@shared_task()
def create_event_records():
    """
    Creates event records from single or recurring events
    :return:
    """
    # Get all the events whose next day is between now and EVENTS_NUM_DAYS_RECORD_LOOK_AHEAD
    # Once a record has been made, update the next_date field taking into account the end_date
    now = timezone.now()
    look_ahead_date = now + timedelta(days=EVENTS_NUM_DAYS_RECORD_LOOK_AHEAD)
    event_records = []

    events = Event.objects.filter(next_date__range=(now, look_ahead_date)).only('cron_recurrence_format', 'next_date',
                                                                                'start_date', 'start_time', 'end_date')
    for event in events:
        next_datetime = datetime.combine(event.next_date, event.start_time)
        event_records.append(EventRecord(event=event, date=next_datetime))
        if event.cron_recurrence_format:
            cron = croniter(event.cron_recurrence_format, next_datetime)
            next_datetime = cron.get_next(ret_type=datetime)
            if next_datetime.date() > event.end_date:
                event.next_date = None
            else:
                event.next_date = next_datetime.date()
        else:
            event.next_date = None
        event.save(update_fields=['next_date'])

    EventRecord.objects.bulk_create(event_records)
