from __future__ import absolute_import

import logging
from datetime import datetime

from celery import shared_task

from events.models import DraftEvent
from events.eventparsers import get_sfkids_events, get_redtri_events

# Get an instance of a logger
logger = logging.getLogger(__name__)


"""
Number of days before which an event for the date should be created
"""
EVENTS_NUM_DAYS_LOOK_AHEAD = 12

@shared_task
def scrape_events_look_ahead():
    start_time = datetime.today()
    events = get_sfkids_events(EVENTS_NUM_DAYS_LOOK_AHEAD)
    for parsed_event in events:
        title = parsed_event.get('title', None)
        url = parsed_event.get('orig_link', None)
        draft_event, created = DraftEvent.objects.get_or_create(title=title, raw=parsed_event,
                                                                source=DraftEvent.SFKIDS, source_url=url)

    events = get_redtri_events(EVENTS_NUM_DAYS_LOOK_AHEAD)
    for parsed_event in events:
        title = parsed_event.get('title', None)
        url = parsed_event.get('orig_link', None)
        draft_event, created = DraftEvent.objects.get_or_create(title=title, raw=parsed_event,
                                                                source=DraftEvent.REDTRI, source_url=url)
    end_time = datetime.today()

    print "Now mail all the events parsed between {} and {}".format(start_time, end_time)

