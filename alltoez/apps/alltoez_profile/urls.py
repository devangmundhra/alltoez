from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib import admin

from forms import UserProfileForm
from views import UserProfileUpdate

urlpatterns = patterns('',
	url(r'^profile/edit/$', UserProfileUpdate.as_view(), {}, name="edit_profile"),
)
