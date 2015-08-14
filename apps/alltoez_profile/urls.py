from allauth.account import views
from django.conf.urls import patterns, url, include
from views import UserProfileUpdate, UserProfileDetail, AlltoezSignupView




from apps.alltoez_profile import api as api_view


urlpatterns = patterns(
                       url(r"^password/change/$", views.password_change, name="account_change_password"),
                       url(r'^profile/edit/$', UserProfileUpdate.as_view(), {"source": "profile_edit"},
                           name="edit_profile"),
                       url(r"^profile/(?P<username>[\w-]+)/$", UserProfileDetail.as_view(), name="show_profile"),
                       url(r'^profile/$', UserProfileDetail.as_view(), name="show_profile"),
                       url(r'^signup/$', AlltoezSignupView.as_view(), {}, name="alltoez_account_signup"),
                       url(r'^signup/step-2/$', UserProfileUpdate.as_view(), {"source": "step2"},
                           name="register_children"),
                       )
