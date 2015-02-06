__author__ = 'devangmundhra'

from django.contrib.auth.models import User
from django.conf import settings

import predictionio

from apps.events.models import Event
from apps.user_actions.models import Bookmark, Done, View


def import_events():
    """
    Reads data from the database about different user_events and sends user_action events to PredictionIO
    :return: Nothing
    """
    pio_access_key = getattr(settings, 'PIO_ACCESS_KEY', None)
    pio_eventserver = getattr(settings, 'PIO_EVENT_SERVER_ENDPOINT', None)

    if not pio_access_key or not pio_eventserver:
        print "PredictionIO not configured"
        return

    event_client = predictionio.EventClient(
        access_key=pio_access_key,
        url=pio_eventserver,
        threads=5,
        qsize=500)

    # Get all users
    for user in User.objects.all():
        event_client.set_user(user.id, event_time=user.date_joined)

    # Get all events
    for event in Event.objects.all():
        event_client.create_event(event="$set", entity_type="item", entity_id=event.id,
                                  properties={'categories': list(event.category.values_list('name', flat=True))},
                                  event_time=event.created_at)

    # Get all user actions
    ## Bookmark
    for user_action in Bookmark.objects.all():
        event_client.create_event(event='bookmark', entity_type='user', entity_id=user_action.user.id,
                                  target_entity_type="item", target_entity_id=user_action.event.id,
                                  event_time=user_action.created)
    ## Done
    for user_action in Done.objects.all():
        event_client.create_event(event='done', entity_type='user', entity_id=user_action.user.id,
                                  target_entity_type="item", target_entity_id=user_action.event.id,
                                  event_time=user_action.created)
    ## View
    for user_action in View.objects.all():
        event_client.create_event(event='view', entity_type='user', entity_id=user_action.user.id,
                                  target_entity_type="item", target_entity_id=user_action.event.id,
                                  event_time=user_action.created)
    event_client.close()

    print "Done with sending events"


def _send_query(events_list):
    """
    Queries PredictionIO Engine for items
    :param events_list: Items which are liked by the user
    :return: Event ids recommended by the engine
    """
    pio_engine = getattr(settings, 'PIO_ENGINE_ENDPOINT', None)

    if not pio_engine:
        return []
    
    engine_client = predictionio.EngineClient(url=pio_engine)
    items_set = set()
    categories_set = set()

    for event in events_list:
        items_set.add(event.id)
        categories_set = categories_set.union(set(event.category.values_list('name', flat=True)))

    try:
        result = engine_client.send_query({"items": list(items_set), "num": 3,
                                           "categories": list(categories_set)})
    except predictionio.NotFoundError:
        print "Recommendation engine not found"
        return []
    events = result.get('itemScores', [])
    return [e['item'] for e in events]


def get_recommended_events(user):
    """
    Get recommended events for this user
    :param user: User for whom recommendations are needed
    :return: list of ids of recommended events
    """
    bookmarked = user.bookmark_set.all()
    done = user.done_set.all()

    events = set(bookmarked.values_list('event__id', flat=True)) | set(done.values_list('event__id', flat=True))

    if not events:
        print "Not enough events to recommend"
    else:
        return _send_query(list(events))


def get_similar_events(event):
    """
    Get recommended events for this user
    :param event: Event for which similar events are being requested
    :return: list of ids of recommended events
    """
    return _send_query([event])