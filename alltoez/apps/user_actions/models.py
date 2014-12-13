from django.db import models
from django.contrib.auth.models import User

from apps.alltoez.utils.abstract_models import BaseModel
from apps.events.models import Event


class UserEventActionsAbstractModel(BaseModel):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)

    class Meta:
        abstract = True


class View(UserEventActionsAbstractModel):
    """
    View: events viewed by user
    """
    pass


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