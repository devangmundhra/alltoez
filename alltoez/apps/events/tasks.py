from __future__ import absolute_import

import logging
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.text import MIMEText
from croniter import croniter
from celery import shared_task

from django.utils import timezone

from apps.events.models import DraftEvent, Event, EventRecord
from apps.events.eventparsers import sfkids, redtri

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
    sfkids_events = sfkids.get_events(EVENTS_NUM_DAYS_SCRAPE_LOOK_AHEAD)
    sfkids_count = 0
    for parsed_event in sfkids_events:
        title = parsed_event.get('title', None)
        url = parsed_event.get('orig_link', None)
        draft_event, created = DraftEvent.objects.get_or_create(title=title,
                                                                raw=json.dumps(parsed_event, ensure_ascii=True),
                                                                source=DraftEvent.SFKIDS, source_url=url)
        if created:
            sfkids_count += 1

    redtri_events = redtri.get_events(EVENTS_NUM_DAYS_SCRAPE_LOOK_AHEAD)
    redtri_count = 0
    for parsed_event in redtri_events:
        title = parsed_event.get('title', None)
        url = parsed_event.get('orig_link', None)
        draft_event, created = DraftEvent.objects.get_or_create(title=title,
                                                                raw=json.dumps(parsed_event, ensure_ascii=True),
                                                                source=DraftEvent.REDTRI, source_url=url)
        if created:
            redtri_count += 1

    subject = "Alltoez draft events | {}".format(today.strftime("%A, %d. %B %Y"))
    body = "New unprocessed events on {} for date {}\n{} through SFKids\n{} through Redtri".format(
        today.strftime("%A, %d. %B %Y"),
        event_date.strftime("%A, %d. %B %Y"),
        sfkids_count, redtri_count)

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "noreply@sandboxe9f734d40d854192ac1344226e7b5125.mailgun.org"
    msg['To'] = "devangmundhra@gmail.com"

    s = smtplib.SMTP('smtp.mailgun.org', 587)

    s.login('postmaster@sandboxe9f734d40d854192ac1344226e7b5125.mailgun.org', '3c8af3c9310cbde4d2e43b3e66e07948')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

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
        event_records += EventRecord(event=event, date=next_datetime)
        if event.cron_recurrence_format is not None:
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