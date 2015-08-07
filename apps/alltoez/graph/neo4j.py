__author__ = 'devangmundhra'

from datetime import datetime
import calendar

from django.db.models import Q
from django.utils import timezone
from django.conf import settings

from apps.alltoez.graph import *

from apps.alltoez_profile.models import UserProfile
from apps.events.models import Event, Category
from apps.venues.models import Venue
from apps.user_actions.models import Bookmark, Done


def update_graph(delete_graph=False, update_schema=False):
    if delete_graph:
        neo4j_graph.delete_all()

    if update_schema:
        neo4j_graph.schema.create_uniqueness_constraint(Event.GRAPH_NODE_NAME, "id")
        neo4j_graph.schema.create_uniqueness_constraint(Category.GRAPH_NODE_NAME, "id")
        neo4j_graph.schema.create_uniqueness_constraint(Venue.GRAPH_NODE_NAME, "id")
        neo4j_graph.schema.create_uniqueness_constraint(UserProfile.GRAPH_USER_NODE_NAME, "id")
        neo4j_graph.schema.create_uniqueness_constraint(UserProfile.GRAPH_FBUSER_NODE_NAME, "id")

    # Add all users and fbusers/friends to graphs
    for user_profile in UserProfile.objects.all():
        user_profile.create_graph_node()

    # Add all categories to graph
    for category in Category.objects.all():
        category.create_graph_node()

    '''
    Don't add all venues for now (to prevent paying for Graphene Pro)
    # Add all venues to graph
    for venue in Venue.objects.all():
        venue.create_graph_node()
    '''

    # Add all events to graph
    for event in Event.objects.filter(Q(end_date__gte=timezone.now()) | Q(end_date=None)):
        event.create_graph_node()

    # Add all user actions to graph
    for bookmark in Bookmark.objects.all():
        bookmark.create_relationship()

    for done in Done.objects.all():
        done.create_relationship()


def get_similar_events(event=None, limit=5, skip=0):
    if settings.DEBUG:
        events = Event.objects.all()[skip:skip+limit]
        return events

    SIMILAR_EVENT = "similar_event"
    now_dt = datetime.now()
    now_utc = calendar.timegm(now_dt.timetuple())
    statement = """
                MATCH (event:Event {{id:{0}}})-[:CATEGORY]-(category:Category)-[:CATEGORY]-({1})
                WHERE event <> {1} AND {1}.start_date < {2} AND {1}.end_date > {2}
                RETURN {1}, count({1}) as event_count
                ORDER BY event_count DESC
                SKIP {3}
                LIMIT {4}
                """.format(event.id, SIMILAR_EVENT, now_utc, skip, limit)
    results = neo4j_graph.cypher.execute(statement)
    similar_event_ids = map(lambda result: result[SIMILAR_EVENT]['id'], results)
    events = Event.objects.all().filter(id__in=similar_event_ids)
    return events
