from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLogin
from rest_framework import viewsets, permissions

from django.http import Http404
from django.contrib.auth.models import User

from .import serializers
from apps.alltoez_profile.models import Child, UserProfile
from common.mixins import UserRequired


class UserRegisterViewSet(viewsets.ModelViewSet):
    """
    View set for registration.
    :parameter     email
    :parameter     password
    """
    http_method_names = ['post']
    serializer_class = serializers.UserRegisterSerializer
    queryset = User.objects.all()


class FacebookLogin(SocialLogin):
    """
    View for facebook login/signup.
    :parameter     facebook access token
    """
    adapter_class = FacebookOAuth2Adapter


class ProfileEditViewSet(UserRequired, viewsets.ModelViewSet):
    """
    View set to update profile of current user.
    """
    http_method_names = ['put', 'get']
    serializer_class = serializers.UpdateUserSerializer
    queryset = UserProfile.objects.all()

    def update(self, request, *args, **kwargs):

        """
        Update method to check the url. to support edit
        """
        if self.kwargs.get('pk') != "update":
            raise Http404
        return super(ProfileEditViewSet, self).update(request, *args, **kwargs)

    def get_object(self):
        """
        Get user object.
        """
        return UserProfile.objects.get(user=self.request.user.id)

    def get_queryset(self):
        if not self.kwargs.get('pk'):
            raise Http404
        return super(ProfileEditViewSet, self).get_queryset()

class ChildUpdateViewSet(UserRequired,viewsets.ModelViewSet):
    """
    View set for child update.
    :parameter     user
    :parameter     first_name
    :parameter     last_name
    :parameter     child name
    :parameter     gender
    :parameter     age
    """
    http_method_names = ('post', 'get' )
    serializer_class = serializers.ChildSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):

        """
        Update method to check the url. to support edit
        """
        if self.kwargs.get('pk') != "update":
            raise Http404
        return super(ChildUpdateViewSet, self).update(request, *args, **kwargs)

    def get_object(self):
        """
        Get user object.
        """
        return UserProfile.objects.get(user=self.request.user.id)

    def get_queryset(self):
        if not self.kwargs.get('pk'):
            raise Http404
        return super(ChildUpdateViewSet, self).get_queryset()


