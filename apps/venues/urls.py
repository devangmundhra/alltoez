__author__ = 'devangmundhra'

from django.conf.urls import patterns, url

from apps.venues.api.views import VenueDetailView

urlpatterns = patterns('',
    url(r"^sfbay/(?P<slug>[\w-]+)/$", VenueDetailView.as_view(), name="venue_detail"),
)