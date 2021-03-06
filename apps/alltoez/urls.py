from django.conf.urls import url, patterns, include
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from rest_framework import routers
from haystack.views import search_view_factory
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

from apps.alltoez.api.views import UserViewSet
from apps.venues.api.views import VenueViewSet
from apps.user_actions.api.views import DoneViewSet, BookmarkViewSet, ReviewViewSet
from apps.alltoez.views import home, AlltoezSearchView, autocomplete
from apps.events.models import Event
from apps.alltoez.sitemaps import StaticViewSitemap
from apps.alltoez_profile.api.views import FacebookLogin, UserRegisterViewSet, SocialAccountDiscontinueViewSet, \
    ChildUpdateViewSet
from apps.events.api.views import EventViewSet, CategoryViewSet, EventSearchViewSet

router = routers.DefaultRouter()
router.register(r'events', EventViewSet, base_name='event')
router.register(r'category', CategoryViewSet)
router.register(r'venues', VenueViewSet)
router.register(r'done', DoneViewSet)
router.register(r'bookmark', BookmarkViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'users', UserViewSet)
router.register(r'signup', UserRegisterViewSet)
router.register(r'child', ChildUpdateViewSet)
router.register(r'disconnect_profile', SocialAccountDiscontinueViewSet, base_name='disconnect_profile')
router.register("search", EventSearchViewSet, base_name="event-search")


sqs = SearchQuerySet().filter(end_date__gte=timezone.now().date()).facet('categories').\
    facet('city',).facet('neighborhood',)

info_dict = {
    'queryset': Event.objects.all().filter(publish=True),
    'date_field': 'published_at',
}

urlpatterns = patterns('',
    url(r"^$", home,  name="home"),
    url('^about/$', TemplateView.as_view(template_name='alltoez/about.html'), name="about-alltoez"),
    url('^privacy/$', TemplateView.as_view(template_name='alltoez/privacy.html'), name="privacy-alltoez"),
    url('^teach/$', TemplateView.as_view(template_name='alltoez/survey/teach.html'), name="tutor-survey"),
    url('^parents/$', TemplateView.as_view(template_name='alltoez/survey/parents.html'), name="parents-survey"),
    url(r'^search/autocomplete/', autocomplete, name="search_autocomplete"),
    url(r'^search/', search_view_factory(
        view_class=AlltoezSearchView,
        form_class=FacetedSearchForm,
        template='alltoez/search/search.html',
        searchqueryset=sqs,
        ), name='search'),
    url(r'^api/v1/', include(router.urls, namespace='api')),
    url(r'^api/v1/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    #url(r'^confirmemail/$',api_views.ConfirmEmailView.as_view(),name='confirmemail'),
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'events': GenericSitemap(info_dict, priority=0.6), 'static': StaticViewSitemap}},
        name='django.contrib.sitemaps.views.sitemap')
)
