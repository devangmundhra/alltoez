from django.conf.urls import url, patterns

from views import Home, Events, Contact, EventDetailView

urlpatterns = patterns('',
    url(r"^$", Home.as_view(),  name="home"),
    url(r"^events/$", Events.as_view(), {'slug':None}, name="events"),
    url(r"^events/(?P<slug>[\w-]+)/$", Events.as_view(), name="events"),
    url(r"^event/(?P<slug>[\w-]+)/$", EventDetailView.as_view(), name="event_detail"),
    url(r"^contact/$", Contact.as_view(),  name="contact"),
)
