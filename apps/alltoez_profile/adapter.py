__author__ = 'devangmundhra'
from django.http import HttpResponse
from django.dispatch import receiver
from django.shortcuts import redirect
from django.conf import settings

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.utils import perform_login, get_login_redirect_url
from allauth.utils import get_user_model
from allauth.socialaccount import app_settings


class AlltoezAccountAdapter(DefaultAccountAdapter):
    pass


class AlltoezSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Login and redirect
        This is done in order to tackle the situation where user's email retrieved
        from one provider is different from already existing email in the database
        (e.g facebook and google both use same email-id). Specifically, this is done to
        tackle following issues:
        * https://github.com/pennersr/django-allauth/issues/215
        """
        email_address = sociallogin.account.extra_data.get('email', None)
        if not email_address:
            return
        try:
            user = get_user_model().objects.get(email=email_address)
            perform_login(request, user, email_verification=app_settings.EMAIL_VERIFICATION)
            if not sociallogin.is_existing:
                sociallogin.connect(request, user)
            raise ImmediateHttpResponse(redirect(get_login_redirect_url(request)))
        except get_user_model().DoesNotExist:
            pass
