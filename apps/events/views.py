import json

from django.utils import timezone, six
from django.views.generic import DetailView, ListView
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

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
    radius_mi = 20
    request = None
    paginate_by = 21
    location_available = False
    location_string = ""

    def get(self, request, *args, **kwargs):
        # default sort is "-created_at"
        self.ordering = self.request.GET.get('sort')
        if not self.ordering:
            self.ordering = self.request.session.get('event_sort', '-published_at')
        else:
            self.request.session['event_sort'] = self.ordering

        self.category_slug = kwargs.get('cat_slug', None)
        self.category_list = Category.objects.filter(parent_category__isnull=False)

        return super(Events, self).get(request, *args, **kwargs)

    def get_queryset(self):
        er = EventsResource()
        request_bundle = er.build_bundle(request=self.request)
        queryset = er.obj_get_list(request_bundle).prefetch_related('category')
        if self.ordering == 'distance':
            if self.request.COOKIES.get('latitude', None) and self.request.COOKIES.get('longitude', None):
                origin = Point(float(self.request.COOKIES['longitude']), float(self.request.COOKIES['latitude']))
                queryset = queryset.filter(venue__point__distance_lte=(origin, D(mi=self.radius_mi))).\
                    distance(origin, field_name='venue__point')
                self.location_string = "current location"
            elif self.request.user.is_authenticated():
                origin = self.request.user.profile.point
                queryset = queryset.filter(venue__point__distance_lte=(origin, D(mi=self.radius_mi))).\
                    distance(origin, field_name='venue__point')
                self.location_string = "%s, %s".format(self.request.user.profile.city, self.request.user.profile.zipcode)
            else:
                self.ordering = ''
        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)
            try:
                self.category = Category.objects.get(slug=self.category_slug)
            except Category.DoesNotExist:
                pass

        """
        TO BE REMOVED WHEN MOVING TO DJANGO 1.8
        START
        """
        ordering = self.ordering
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        """
        TO BE REMOVED WHEN MOVING TO DJANGO 1.8
        END
        """
        self.queryset = queryset
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

        if self.request.user.is_authenticated() \
                or (self.request.COOKIES.get('latitude', None) and self.request.COOKIES.get('longitude', None)):
            self.location_available = True

        context['now'] = timezone.now()
        context['events_list'] = json.loads(list_json)
        context['category_list'] = self.category_list
        context['category'] = self.category
        context['event_sort'] = self.ordering
        context['venue_radius'] = self.radius_mi
        context['page_template'] = self.page_template
        context['location_available'] = self.location_available
        context['location_string'] = self.location_string
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
        from apps.user_actions.tasks import mark_user_views_event, new_action
        self.object = self.get_object()
        if request.user.is_authenticated():
            mark_user_views_event.delay(self.object.id, request.user.id)
        else:
            new_action.delay("View", None, self.object.id, request.META['REMOTE_ADDR'])
        context = self.get_context_data(object=self.object)
        er = EventsResource()
        er_bundle = er.build_bundle(obj=self.object, request=request)
        event_json = er.serialize(None, er.full_dehydrate(er_bundle), 'application/json')
        event = json.loads(event_json)
        context['event'] = event
        context['event_json'] = event_json # Needed for parsing bookmark info in event_detail template
        return self.render_to_response(context)