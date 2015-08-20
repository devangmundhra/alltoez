from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLogin
from rest_framework import viewsets, permissions,mixins,status

from django.http import Http404
from django.contrib.auth.models import User

from .import serializers
from rest_framework.response import Response
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


class ChildUpdateViewSet(UserRequired, viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = serializers.ChildSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        children = request.DATA['children']
        serializer = self.get_serializer(data=children, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
