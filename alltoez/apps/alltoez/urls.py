from django.conf.urls import url, patterns, include

from tastypie.api import Api
from haystack.views import search_view_factory
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

from apps.user_actions.api import BookmarkResource, DoneResource
from apps.alltoez.api import EventsResource, AlltoezProfileResource
from apps.alltoez.views import home, AlltoezSearchView

v1_api = Api(api_name='v1')
v1_api.register(EventsResource())
v1_api.register(BookmarkResource())
v1_api.register(DoneResource())
v1_api.register(AlltoezProfileResource())

sqs = SearchQuerySet().facet('categories')

urlpatterns = patterns('',
    url(r"^$", home,  name="home"),
    url(r'^search/', search_view_factory(
        view_class=AlltoezSearchView,
        form_class=FacetedSearchForm,
        template='alltoez/search/search.html',
        searchqueryset=sqs,
        ), name='search'),
    # url(r"^contact/$", Contact.as_view(),  name="contact"),
    url(r'^api/', include(v1_api.urls)),
)
