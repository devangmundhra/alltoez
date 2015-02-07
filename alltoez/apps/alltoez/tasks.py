__author__ = 'devangmundhra'

import logging

from django.db.models import Q
from django.utils import timezone

from celery import shared_task

from apps.events.models import Event, SimilarEvents
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