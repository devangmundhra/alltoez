__author__ = 'devangmundhra'

from django.contrib.auth.models import User

from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.cache import SimpleCache

from apps.alltoez_profile.models import UserProfile, Child


class ChildInternalResource(ModelResource):
    """
    Child Resource
    Internal resource. Exposed only via profile.
    """
    class Meta:
        resource_name = "children_internal"
        queryset = Child.objects.all()
        authentication = SessionAuthentication()
        cache = SimpleCache(timeout=100)


class UserInternalResource(ModelResource):
    """
    UserResource
    Internal resource. Exposed only via profile.
    """
    children = fields.ToManyField(ChildInternalResource, 'children', full=True)

    class Meta:
        resource_name = 'users_internal'
        queryset = User.objects.all()
        authentication = SessionAuthentication()
        fields = ['username', 'first_name', 'last_name', 'email', 'children']
        allowed_methods = ['get']
        cache = SimpleCache(timeout=100)


class AlltoezProfileInternalResource(ModelResource):
    """
    Internal resource not directly exposed by the api
    This resource is exposed via the AlltoezProfileResource in apps.alltoez.api
    """
    user = fields.ToOneField(UserInternalResource, 'user', full=True)

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'users'
        authentication = SessionAuthentication()
        excludes = ['latitude', 'longitude', 'address', 'address_line_2', 'address_line_3', 'created', 'updated']
        cache = SimpleCache(timeout=100)
