from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie import fields
from tastypie.exceptions import Unauthorized
from tastypie.cache import SimpleCache

from apps.user_actions.models import View, Bookmark, Done, Share
from apps.alltoez_profile.api import UserInternalResource
from apps.events.api import EventInternalResource


class UserActionAuthorization(Authorization):
    """
    Authorization class for user action. It is to be used in conjunction with an Authentication class.
    Permission granted as follows-
    Create: Allow any user to create
    Read: Any user is allowed to read
    Update: Only the user associated with the model is allowed to update
    Delete: Only the user associated with the model is allowed to delete
    """
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.all()

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return True

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


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
        authorization = UserActionAuthorization()
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