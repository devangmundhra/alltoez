from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib import admin

from forms import UserProfileForm
from views import UserProfileUpdate, RegisterChild, AlltoezSignupView

urlpatterns = patterns('',
	# url(r'^profile/edit/$', UserProfileUpdate.as_view(), {}, name="edit_profile"),
    url(r'^signup/step-2/$', UserProfileUpdate.as_view(), name="register_children"),
    url(r'^signup/$', AlltoezSignupView.as_view(), {}, name="alltoez_account_signup"),
)