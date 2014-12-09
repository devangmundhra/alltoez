from django.conf.urls import url, patterns, include

from tastypie.api import Api

from apps.user_actions.api import BookmarkResource, DoneResource
from apps.alltoez.api import EventsResource
from apps.alltoez.views import home, Home, Events, EventDetailView

v1_api = Api(api_name='v1')
v1_api.register(EventsResource())
v1_api.register(BookmarkResource())
v1_api.register(DoneResource())

urlpatterns = patterns('',
    url(r"^$", home,  name="home"),
    url(r"^events/", include([
        url(r"^$", Events.as_view(page_template="alltoez/events/event_list_page.html"), {'cat_slug': None}, name="events"),
        url(r"^(?P<cat_slug>[\w-]+)/$", Events.as_view(page_template="alltoez/events/event_list_page.html"), name="events"),
        url(r"^san-francisco/(?P<slug>[\w-]+)/$", EventDetailView.as_view(), name="event_detail"),
    ])),
    # url(r"^contact/$", Contact.as_view(),  name="contact"),
    url(r'^api/', include(v1_api.urls)),
)
