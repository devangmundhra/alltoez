from django.core.mail import EmailMessage
from django.http import Http404
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from rest_auth.registration.views import SocialLogin,ConfirmEmailView
from rest_framework import viewsets, permissions,mixins,status
from rest_framework.response import Response
from rest_framework.views import APIView


from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.account.forms import LoginForm
import requests

from apps.alltoez_profile.models import Child, UserProfile
from apps.alltoez.serializers import AllauthSerializer
from allauth.socialaccount.models import SocialAccount, SocialToken
from .import serializers
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        email_address = serializer.data['username']
        msg = EmailMessage(from_email=("Alltoez", "noreply@alltoez.com"),
                       to=[email_address])
        msg.template_name = "Welcome To Alltoez"
        msg.send()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VerifyEmailViewSet(UserRequired, APIView, ConfirmEmailView):

    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        self.kwargs['key'] = self.request.DATA.get('key', '')
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)


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
        userss = request.user
        print userss,'aaaaaaaaaaaaaaaa'
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


class SocialAccountDiscontinueViewSet(UserRequired, viewsets.ModelViewSet):
    """
    Deletes and disconnects the linked social account to the web.
    """
    http_method_names = ['delete']

    serializer_class = AllauthSerializer
    model = SocialAccount

    def perform_destroy(self, instance):
        instance.delete() # uncomment to get the social account deleted
        self.disconnect()

    def get_queryset(self):
        return self.model.objects.filter(user = self.request.user)

    def disconnect(self, *args, **kwargs):
        """
        Disconnects the social account.
        :param args:
        :param kwargs:
        :return: object, object
        """
        account, token_obj = self._get_social_account()  # retrieving  social info
        revoke_url = 'https://graph.facebook.com/{uid}/permissions'.format(uid=account.uid)
        params = {'access_token': token_obj.token}
        response = requests.delete(revoke_url,  params=params)

        return response

    def _get_social_account(self):
        account = SocialAccount.objects.get(user__id=self.request.user.id)
        token = SocialToken.objects.get(account=account)
        return account, token


class ChildUpdateViewSet(UserRequired, viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = serializers.ChildSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print request.DATA, "oooooooooooooooooooooo"
        children = request.DATA['children']
        serializer = self.get_serializer(data=children, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HomePageTemplateView(APIView):
    """
    View for returning home page html content
    """
    http_method_names = ['get']
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        """
        Returns the home page template division.
        """

        template = render_to_string(template_name='home.html', request=request)

        return Response(template)


class LoginPageTemplateView(APIView):
    """
    View for returning login page html content
    """
    http_method_names = ['get']
    permission_classes = (permissions.AllowAny,)

    def get(self,request,format=None):
        """

        Returns the login page template view
        """
        form = LoginForm()
        template = render_to_string(template_name='login.html', request=request, context={'form':form})

        return Response(template)


class EventPageTemplateView(APIView):
    """
    View for returning login page html content
    """
    http_method_names = ['get']
    permission_classes = (permissions.AllowAny,)

    def get(self,request,format=None):
        """

        Returns the Event page template view
        """

        template = render_to_string(template_name='event.html', request=request)

        return Response(template)
