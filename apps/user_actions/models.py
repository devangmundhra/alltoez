from django.db import models
from django.contrib.auth.models import User

from apps.alltoez.graph import *
from apps.alltoez.utils.abstract_models import BaseModel
from apps.events.models import Event
from apps.alltoez_profile.models import UserProfile


class GraphName(object):
    class NodeLabel(object):
        pass

    class Relationship(object):
        BOOKMARK = "BOOKMARK"
        DONE = "Done"


class UserEventActionsAbstractModel(BaseModel):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)

    class Meta:
        abstract = True
        app_label = 'user_actions'


class View(UserEventActionsAbstractModel):
    """
    View: events viewed by user
    """
    pass


class ViewIP(models.Model):
    """
    ViewIP: events viewed by ipaddress
    """
    ip_address = models.GenericIPAddressField(db_index=True)
    event = models.ForeignKey(Event)
    count = models.IntegerField(default=0)

    class Meta:
        app_label = 'user_actions'
        unique_together = ('ip_address', 'event')


class Bookmark(UserEventActionsAbstractModel):
    """
    Bookmark: events bookmarked by user
    """
    GRAPH_USER_EVENT_RELATIONSHIP = "BOOKMARK"

    class Meta(UserEventActionsAbstractModel.Meta):
        unique_together = ('user', 'event')

    def create_relationship(self):
        event_node = neo4j_graph.merge_one(Event.GRAPH_NODE_NAME, "id", self.event.id)
        user_node = neo4j_graph.merge_one(UserProfile.GRAPH_USER_NODE_NAME, "id", self.user.id)
        neo4j_graph.create_unique(Relationship(event_node, Bookmark.GRAPH_USER_EVENT_RELATIONSHIP, user_node))

    @classmethod
    def drop_relationship(cls, event_id, user_id):
        event_node = neo4j_graph.merge_one(Event.GRAPH_NODE_NAME, "id", event_id)
        user_node = neo4j_graph.merge_one(UserProfile.GRAPH_USER_NODE_NAME, "id", user_id)
        rel = neo4j_graph.match_one(event_node, Bookmark.GRAPH_USER_EVENT_RELATIONSHIP, user_node)
        neo4j_graph.delete(rel)


class Done(UserEventActionsAbstractModel):
    """
    Done: events done by user
    """
    GRAPH_USER_EVENT_RELATIONSHIP = "DONE"

    class Meta(UserEventActionsAbstractModel.Meta):
        unique_together = ('user', 'event')

    def create_relationship(self):
        event_node = neo4j_graph.merge_one(Event.GRAPH_NODE_NAME, "id", self.event.id)
        user_node = neo4j_graph.merge_one(UserProfile.GRAPH_USER_NODE_NAME, "id", self.user.id)
        neo4j_graph.create_unique(Relationship(event_node, Done.GRAPH_USER_EVENT_RELATIONSHIP, user_node))

    @classmethod
    def drop_relationship(cls, event_id, user_id):
        event_node = neo4j_graph.merge_one(Event.GRAPH_NODE_NAME, "id", event_id)
        user_node = neo4j_graph.merge_one(UserProfile.GRAPH_USER_NODE_NAME, "id", user_id)
        rel = neo4j_graph.match_one(event_node, Done.GRAPH_USER_EVENT_RELATIONSHIP, user_node)
        neo4j_graph.delete(rel)


class Share(UserEventActionsAbstractModel):
    """
    Share: events shared by user
    """
    pass


class Review(UserEventActionsAbstractModel):
    """
    Review: review and comment for an event
    """
    RATING_CHOICES = (
        (0, 'No Rating'),
        (1, 'One Star'),
        (2, 'Two Star'),
        (3, 'Three Star'),
        (4, 'Four Star'),
        (5, 'Five Star')
    )
    rating = models.PositiveSmallIntegerField(verbose_name="rating", choices=RATING_CHOICES, default=0)
    comment = models.TextField(blank=False, null=False)

    class Meta(UserEventActionsAbstractModel.Meta):
        unique_together = ('user', 'event')