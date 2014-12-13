from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie import fields

from apps.user_actions.models import View, Bookmark, Done, Share
from apps.alltoez_profile.api import UserInternalResource
from apps.events.api import EventInternalResource


class UserActionAbstractResource(ModelResource):
    """
    UserActionAbstractResource
    Abstract resource for all user action models
    """
    event = fields.ForeignKey(EventInternalResource, 'event', full=False)
    user = fields.ForeignKey(UserInternalResource, 'user', full=False)

    class Meta:
        resource_name = 'abstract_user_action'
        abstract = True
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        always_return_data = True

    def hydrate_user(self, bundle):
        bundle.data['user'] = bundle.request.user
        return bundle


class BookmarkResource(UserActionAbstractResource):
    """
    BookmarkResource
    """
    class Meta(UserActionAbstractResource.Meta):
        resource_name = 'bookmark'
        queryset = Bookmark.objects.all()


class DoneResource(UserActionAbstractResource):
    """
    DoneResource
    """
    class Meta(UserActionAbstractResource.Meta):
        resource_name = 'done'
        queryset = Done.objects.all()


class ViewResource(UserActionAbstractResource):
    """
    ViewResource
    """
    class Meta(UserActionAbstractResource.Meta):
        resource_name = 'view'
        queryset = View.objects.all()


class ShareResource(UserActionAbstractResource):
    """
    ShareResource
    """
    class Meta(UserActionAbstractResource.Meta):
        resource_name = 'share'
        queryset = Share.objects.all()