import json

from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Polygon
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
import keen

from apps.events.serializers import CategorySerializer, EventInternalSerializer
from apps.events.models import Event, Category
from apps.alltoez.utils.geo import rev_geocode_location_component

"""
API Endpoint for Events module
"""


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EventInternalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventInternalSerializer
    ordering = ('-published_at',)
    ordering_fields = ('published_at', 'end_date', 'cost', 'min_age', 'max_age', 'view_count', 'distance')

    def get_queryset(self):
        qs = Event.objects.all().filter(publish=True).filter(Q(end_date__gte=timezone.now()) | Q(end_date=None))
        return qs

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
    request = None
    paginate_by = 21
    location_name = ""
    latitude = None
    longitude = None
    location_available = False
    bounds = None
    zoom = 8

    def get(self, request, *args, **kwargs):
        # default sort is "end_date"
        self.ordering = self.request.GET.get('ordering')
        if not self.ordering:
            self.ordering = self.request.session.get('event_sort', 'end_date')
        else:
            self.request.session['event_sort'] = self.ordering

        bounds = self.request.GET.get('bounds', None)
        self.zoom = self.request.GET.get('zoom', 8)

        if bounds:
            try:
                bounds_list = bounds.split(',')
                sw = (bounds_list[0], bounds_list[1])
                ne = (bounds_list[2], bounds_list[3])
                xmin = sw[1]
                ymin = sw[0]
                xmax = ne[1]
                ymax = ne[0]
                bbox = (xmin, ymin, xmax, ymax)
                self.bounds = Polygon.from_bbox(bbox)
                if self.request.user.is_authenticated():
                    profile = self.request.user.profile
                    profile.last_known_location_bounds = self.bounds
                    profile.last_map_zoom = self.zoom
                    profile.save()
            except IndexError:
                pass
        if not self.bounds and self.request.user.is_authenticated():
            self.bounds = self.request.user.profile.last_known_location_bounds
            self.zoom = self.request.user.profile.last_map_zoom
        if self.bounds:
            centroid = self.bounds.centroid
            self.latitude = centroid.y
            self.longitude = centroid.x
            neighborhood = rev_geocode_location_component(self.latitude, self.longitude, 'neighborhood')
            if not neighborhood:
                #If not succeed in first try, try again (with a bigger net)
                neighborhood = rev_geocode_location_component(self.latitude, self.longitude, 'political')
            city = rev_geocode_location_component(self.latitude, self.longitude, 'locality')
            self.location_name = u"{}, {}".format(neighborhood, city)

        self.category_slug = kwargs.get('cat_slug', None)
        self.category_list = Category.objects.filter(parent_category__isnull=False)

        return super(Events, self).get(request, *args, **kwargs)

    def get_queryset(self):
        from apps.alltoez.views import EventViewSet
        queryset = EventViewSet.get_direct_queryset(self.request)

        # Apply any location filters if needed
        if self.bounds:
            queryset = queryset.filter(venue__point__within=self.bounds).\
                distance(self.bounds.centroid, field_name='venue__point')
            self.location_available = True
            keen.add_event('event_filter', {
                'keen': {
                    'location': {
                        'coordinates': [self.bounds.centroid.x, self.bounds.centroid.y],
                    }
                },
                'category': self.category_slug,
            }, timezone.now())

        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)
            try:
                self.category = Category.objects.get(slug=self.category_slug)
            except Category.DoesNotExist:
                pass

        self.queryset = queryset
        return super(Events, self).get_queryset()

    def get_context_data(self, **kwargs):
        from apps.alltoez.serializers import EventSerializer

        context = super(Events, self).get_context_data(**kwargs)
        events_page = context['page_obj']

        serializer = EventSerializer(events_page.object_list, many=True, context={'request': self.request})

        context['now'] = timezone.now()
        context['events_list'] = json.loads(JSONRenderer().render(serializer.data))
        context['category_list'] = self.category_list
        context['category'] = self.category
        context['event_sort'] = self.ordering
        context['page_template'] = self.page_template
        context['latitude'] = self.latitude
        context['longitude'] = self.longitude
        context['location_available'] = self.location_available
        context['location_string'] = self.location_name
        context['zoom'] = self.zoom if self.zoom else 8
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
        from apps.alltoez.serializers import EventSerializer
        from apps.user_actions.tasks import mark_user_views_event, new_action
        self.object = self.get_object()
        if request.user.is_authenticated():
            mark_user_views_event.delay(self.object.id, request.user.id, request.META['REMOTE_ADDR'])
        else:
            mark_user_views_event.delay(self.object.id, None, request.META['REMOTE_ADDR'])
            new_action.delay("View", None, self.object.id, request.META['REMOTE_ADDR'])
        context = self.get_context_data(object=self.object)
        serializer = EventSerializer(self.object, context={'request': request})
        event_json = JSONRenderer().render(serializer.data)
        event = json.loads(event_json)
        context['event'] = event
        context['event_json'] = event_json # Needed for parsing bookmark info in event_detail template
        context['location_string'] = request.session.get('location_name', 'your location')
        return self.render_to_response(context)
