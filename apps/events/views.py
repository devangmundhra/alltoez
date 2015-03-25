import json

from django.utils import timezone
from django.views.generic import DetailView, ListView

from apps.events.models import Event, Category
from apps.alltoez.api import EventsResource

"""
Alltoez event views
"""


class Events(ListView):
    template_name = 'events/events.html'
    page_template = "events/event_list_page.html"
    category = None
    category_list = None
    category_slug = None
    ordering = None
    radius = None
    request = None
    paginate_by = 21

    def get(self, request, *args, **kwargs):
        # default sort is "-created_at"
        self.ordering = self.request.GET.get('sort')
        if not self.ordering:
            self.ordering = self.request.session.get('event_sort', '-created_at')
        else:
            self.request.session['event_sort'] = self.ordering

        # radius in miles. default is 10m
        self.radius = self.request.GET.get('radius')
        if not self.radius:
            self.radius = self.request.session.get('venue_radius', 10)
        else:
            self.request.session['venue_radius'] = self.radius

        self.category_slug = kwargs.get('cat_slug', None)
        self.category_list = Category.objects.filter(parent_category__isnull=False)

        return super(Events, self).get(request, *args, **kwargs)

    def get_queryset(self):
        er = EventsResource()
        request_bundle = er.build_bundle(request=self.request)
        queryset = er.obj_get_list(request_bundle).prefetch_related('category')
        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)
            try:
                self.category = Category.objects.get(slug=self.category_slug)
            except Category.DoesNotExist:
                pass

        # TODO: Filter the queryset for venue radius using http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
        # TODO: and alltoez.utils.geo

        # Sort by the sort key
        self.queryset = queryset.select_related('venue')
        return super(Events, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(Events, self).get_context_data(**kwargs)
        events_page = context['page_obj']
        er = EventsResource()
        bundles = []
        for obj in events_page.object_list:
            bundle = er.build_bundle(obj=obj, request=self.request)
            bundles.append(er.full_dehydrate(bundle, for_list=True))

        list_json = er.serialize(self.request, bundles, "application/json")

        context['now'] = timezone.now()
        context['events_list'] = json.loads(list_json)
        context['category_list'] = self.category_list
        context['category'] = self.category
        context['event_sort'] = self.ordering
        context['venue_radius'] = self.radius
        context['page_template'] = self.page_template
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


