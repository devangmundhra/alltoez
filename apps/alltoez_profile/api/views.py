import requests
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from rest_auth.registration.views import SocialLoginView, ConfirmEmailView
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.models import SocialAccount, SocialToken

from apps.alltoez.api.serializers import AllauthSerializer
from apps.alltoez_profile.api import serializers
from common.mixins import UserRequired


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
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


class FacebookLogin(SocialLoginView):
    """
    View for facebook login/signup.
    :parameter     facebook access token
    """
    adapter_class = FacebookOAuth2Adapter


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
