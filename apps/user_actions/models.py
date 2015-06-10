from django.db import models
from django.contrib.auth.models import User

from apps.alltoez.utils.abstract_models import BaseModel
from apps.events.models import Event


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

    class Meta(UserEventActionsAbstractModel.Meta):
        unique_together = ('user', 'event')


class Done(UserEventActionsAbstractModel):
    """
    Done: events done by user
    """
    class Meta(UserEventActionsAbstractModel.Meta):
        unique_together = ('user', 'event')


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