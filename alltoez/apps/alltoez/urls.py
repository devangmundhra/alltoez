from django.conf.urls import url, patterns, include

from tastypie.api import Api

from apps.user_actions.api import BookmarkResource, DoneResource
from apps.alltoez.api import EventsResource, AlltoezProfileResource
from apps.alltoez.views import home

v1_api = Api(api_name='v1')
v1_api.register(EventsResource())
v1_api.register(BookmarkResource())
v1_api.register(DoneResource())
v1_api.register(AlltoezProfileResource())

urlpatterns = patterns('',
    url(r"^$", home,  name="home"),
    # url(r"^contact/$", Contact.as_view(),  name="contact"),
    url(r'^api/', include(v1_api.urls)),
)
