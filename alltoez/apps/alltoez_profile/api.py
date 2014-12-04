__author__ = 'devangmundhra'

from django.contrib.auth.models import User
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource


class UserInternalResource(ModelResource):
    """
    UserResource
    """
    class Meta:
        resource_name = 'users_internal'
        queryset = User.objects.all()
        authentication = SessionAuthentication()
