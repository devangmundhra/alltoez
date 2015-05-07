from django.conf.urls import patterns, url

from apps.events.views import Events, EventDetailView

urlpatterns = patterns('',
    url(r"^$", Events.as_view(), {'cat_slug': None}, name="events"),
    url(r"^(?P<cat_slug>[\w-]+)/$", Events.as_view(), name="events"),
    url(r"^san-francisco/(?P<slug>[\w-]+)/$", EventDetailView.as_view(),),
    url(r"^sfbay/(?P<slug>[\w-]+)/$", EventDetailView.as_view(), name="event_detail"),
)
