from PIL.XVThumbImagePlugin import r
from allauth.account import views
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib import admin

from forms import UserProfileForm
from views import UserProfileUpdate, UserProfileDetail, AlltoezSignupView, AlltoezSignupStep2View

urlpatterns = patterns('',
    url(r"^password/change/$", views.password_change, name="account_change_password"),
	url(r'^profile/edit/$', UserProfileUpdate.as_view(), {"source":"profile_edit"}, name="edit_profile"),
    url(r"^profile/(?P<username>[\w-]+)/$", UserProfileDetail.as_view(), name="show_profile"),
    url(r'^signup/$', AlltoezSignupView.as_view(), {}, name="alltoez_account_signup"),
    url(r'^signup/step-2/$', UserProfileUpdate.as_view(), {"source":"step2"}, name="register_children"),
    # url(r'^signup/step-2/$', AlltoezSignupStep2View.as_view(), name="register_children"),
)