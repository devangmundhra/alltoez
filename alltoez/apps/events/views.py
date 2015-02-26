import json
import time

from django.utils import timezone
from django.views.generic import DetailView

from endless_pagination.views import AjaxListView
import newrelic.agent

from apps.events.models import Event, Category

"""
Alltoez event views
"""


class Events(AjaxListView):
    template_name = 'events/events.html'
    page_template = "events/event_list_page.html"
    model = Event
    events_list = None
    category = None
    category_list = None
    category_slug = None
    sort = None
    radius = None
    request = None

    def get(self, request, *args, **kwargs):
        from apps.alltoez.api import EventsResource

        newrelic.agent.record_custom_metric('Custom/Event1', time.time())

        # default sort is "-created_at"
        self.sort = self.request.GET.get('sort')
        if not self.sort:
            self.sort = self.request.session.get('event_sort', '-created_at')
        else:
            self.request.session['event_sort'] = self.sort

        # radius in miles. default is 10m
        self.radius = self.request.GET.get('radius')
        if not self.radius:
            self.radius = self.request.session.get('venue_radius', 10)
        else:
            self.request.session['venue_radius'] = self.radius

        newrelic.agent.record_custom_metric('Custom/Event2', time.time())

        self.category_slug = kwargs.get('cat_slug', None)
        self.category_list = Category.objects.filter(parent_category__isnull=False)

        newrelic.agent.record_custom_metric('Custom/Event3', time.time())

        er = EventsResource()
        request_bundle = er.build_bundle(request=request)
        queryset = er.obj_get_list(request_bundle).prefetch_related('category')

        newrelic.agent.record_custom_metric('Custom/Event4', time.time())
        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)
            try:
                self.category = Category.objects.get(slug=self.category_slug)
            except Category.DoesNotExist:
                pass

        newrelic.agent.record_custom_metric('Custom/Event5', time.time())
        # TODO: Filter the queryset for venue radius using http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
        # TODO: and alltoez.utils.geo

        # Sort by the sort key
        queryset = queryset.order_by(self.sort).select_related('venue')

        newrelic.agent.record_custom_metric('Custom/Event6', time.time())
        bundles = []
        for obj in queryset:
            bundle = er.build_bundle(obj=obj, request=request)
            bundles.append(er.full_dehydrate(bundle, for_list=True))

        newrelic.agent.record_custom_metric('Custom/Event7', time.time())

        list_json = er.serialize(None, bundles, "application/json")
        newrelic.agent.record_custom_metric('Custom/Event8', time.time())
        self.events_list = json.loads(list_json)
        newrelic.agent.record_custom_metric('Custom/Event9', time.time())
        return super(Events, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Events, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['events_list'] = self.events_list
        context['category_list'] = self.category_list
        context['category'] = self.category
        context['event_sort'] = self.sort
        context['venue_radius'] = self.radius
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    object = None

    def get(self, request, *args, **kwargs):
        """
        This method has been copied from django/views/generic/detail.py
        :param request:
        :param args:
        :param kwargs:
        :return: HttpResponse
        """
        from apps.alltoez.api import EventsResource
        from apps.user_actions.tasks import mark_user_views_event
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        er = EventsResource()
        er_bundle = er.build_bundle(obj=self.object, request=request)
        event_json = er.serialize(None, er.full_dehydrate(er_bundle), 'application/json')
        event = json.loads(event_json)
        context['event'] = event
        context['event_json'] = event_json # Needed for parsing bookmark info in event_detail template
        if request.user.is_authenticated():
            mark_user_views_event.delay(self.object.id, request.user.id)
        return self.render_to_response(context)


