from __future__ import absolute_import

__author__ = 'devangmundhra'

import logging

from django.conf import settings
from django.utils import timezone
from django.db.models import F

from celery import shared_task
import predictionio
import keen
from allauth.utils import get_user_model

from apps.user_actions.models import View, ViewIP, Bookmark, Done
from apps.events.models import Event

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Get an instance of prediction io event client
pio_access_key = getattr(settings, 'PIO_ACCESS_KEY', "unknown access key")
pio_eventserver = getattr(settings, 'PIO_EVENT_SERVER_ENDPOINT', "http://localhost:7070")


@shared_task
def mark_user_views_event(event_id, user_id, ip_address):
    if user_id:
        view = View()
        view.event_id = event_id
        view.user_id = user_id
        view.save()

    ipview, created = ViewIP.objects.get_or_create(event_id=event_id, ip_address=ip_address)
    ipview.count = F('count') + 1
    ipview.save()

    # Send info to keen
    staff_status = False
    if user_id:
        try:
            user = get_user_model().objects.get(pk=user_id)
            staff_status = user.is_staff
        except get_user_model().DoesNotExist:
            keen.add_event("Error", {
                "msg": "User.DoesNotExist",
                "id": user_id
            })

    event = Event.objects.get(pk=event_id)

    keen_events = []

    for category in event.category.all():
        keen_events += {
            'view_single': {
                'keen': {
                    'time_stamp': timezone.now(),
                    'location': {
                        'coordinates': [event.venue.longitude, event.venue.latitude],
                    }
                },
                "user": {
                    "user_id": user_id,
                    "staff": staff_status,
                    "ip": ip_address
                },
                "event": {
                    "event_id": event_id,
                    "category": category.name,
                    "min_age": event.min_age,
                    "max_age": event.max_age,
                    "cost": event.cost,
                    "start_date": event.start_date.isoformat(),
                    "end_date": event.end_date.isoformat() if event.end_date else None,
                    "publish_date": event.published_at.isoformat() if event.published_at else None
                },
                "venue": {
                    "venue_id": event.venue.id,
                    "name": event.venue.name,
                    "city": event.venue.city,
                    "neighborhood": event.venue.neighborhood,
                }
            }
        }

    keen.add_events(keen_events)


@shared_task
def new_action(event_type, user_id, event_id, session_id=None):
    """
    Create a new event on pio server
    :param event_type:
    :param user_id:
    :param event_id:
    :param session_id:
    :return:
    """

    staff_status = False
    if user_id:
        try:
            user = get_user_model().objects.get(pk=user_id)
            staff_status = user.is_staff
        except get_user_model().DoesNotExist:
            keen.add_event("Error", {
                "msg": "User.DoesNotExist",
                "id": user_id
            })

    try:
        event = Event.objects.get(pk=event_id)

        keen.add_event(event_type, {
            "user": {
                "user_id": user_id,
                "staff": staff_status,
                "session_id": session_id
            },
            "event": {
                "event_id": event_id,
                "categories": list(event.category.all().values_list('name', flat=True)),
                "min_age": event.min_age,
                "max_age": event.max_age,
                "cost": event.cost,
                "start_date": event.start_date.isoformat(),
                "end_date": event.end_date.isoformat() if event.end_date else None,
                "publish_date": event.published_at.isoformat() if event.published_at else None
            },
            "venue": {
                "venue_id": event.venue.id,
                "name": event.venue.name,
                "city": event.venue.city,
                "neighborhood": event.venue.neighborhood,
            }
        }, timezone.now())
    except Event.DoesNotExist:
        keen.add_event("Error", {
            "msg": "Event.DoesNotExist",
            "id": event_id
        })


def pio_new_event(event_type, user_id, event_id, created):
    """
    Create a new event on pio server
    :param event_type:
    :param user_id:
    :param event_id:
    :param created:
    :return:
    """
    event_client = predictionio.EventClient(
        access_key=pio_access_key,
        url=pio_eventserver,
        threads=5, qsize=500)

    try:
        event_client.record_user_action_on_item(event_type, user_id, event_id,
                                                event_time=created)
        event_client.close()
    except predictionio.NotCreatedError:
        pass


@shared_task
def bookmark_post_save_task(pk):
    try:
        bookmark = Bookmark.objects.get(id=pk)
        bookmark.create_relationship()
    except Bookmark.DoesNotExist:
        pass


@shared_task
def bookmark_post_delete_task(event_id, user_id):
    Bookmark.drop_relationship(event_id, user_id)
    


@shared_task
def done_post_save_task(pk):
    try:
        done = Done.objects.get(id=pk)
        done.create_relationship()
    except Done.DoesNotExist:
        pass


@shared_task
def done_post_delete_task(event_id, user_id):
    Done.drop_relationship(event_id, user_id)