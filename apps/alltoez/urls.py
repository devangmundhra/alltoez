from django.conf.urls import url, patterns, include
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap

from tastypie.api import Api
from haystack.views import search_view_factory
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

from apps.user_actions.api import BookmarkResource, DoneResource, ReviewResource
from apps.alltoez.api import EventsResource, AlltoezProfileResource
from apps.alltoez.views import home, AlltoezSearchView, autocomplete
from apps.events.models import Event
from apps.alltoez.sitemaps import StaticViewSitemap

v1_api = Api(api_name='v1')
v1_api.register(EventsResource())
v1_api.register(BookmarkResource())
v1_api.register(DoneResource())
v1_api.register(ReviewResource())
v1_api.register(AlltoezProfileResource())

sqs = SearchQuerySet().filter(end_date__gte=timezone.now().date()).facet('categories').\
    facet('city',).facet('neighborhood',)

info_dict = {
    'queryset': Event.objects.all().filter(publish=True),
    'date_field': 'published_at',
}

urlpatterns = patterns('',
    url(r"^$", home,  name="home"),
    url('^about/$', TemplateView.as_view(template_name='alltoez/about.html'), name="about-alltoez"),
    url(r'^search/autocomplete/', autocomplete, name="search_autocomplete"),
    url(r'^search/', search_view_factory(
        view_class=AlltoezSearchView,
        form_class=FacetedSearchForm,
        template='alltoez/search/search.html',
        searchqueryset=sqs,
        ), name='search'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'events': GenericSitemap(info_dict, priority=0.6), 'static': StaticViewSitemap}},
        name='django.contrib.sitemaps.views.sitemap')
)
