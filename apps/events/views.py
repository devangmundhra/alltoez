import json

from django.utils import timezone, six
from django.views.generic import DetailView, ListView
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

from apps.events.models import Event, Category
from apps.alltoez.api import EventsResource
from apps.alltoez.utils.geo import rev_geocode_location_component

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
    radius_mi = 7  # 7 miles
    request = None
    paginate_by = 21
    location_available = False
    location_name = ""
    latitude = None
    longitude = None

    def get(self, request, *args, **kwargs):
        # default sort is "-published_at"
        self.ordering = self.request.GET.get('sort')
        if not self.ordering:
            self.ordering = self.request.session.get('event_sort', '-published_at')
        else:
            self.request.session['event_sort'] = self.ordering

        all_bay_area = self.request.GET.get('area', None)
        self.latitude = float(self.request.GET.get('lat', 0))
        self.longitude = float(self.request.GET.get('lng', 0))
        self.radius_mi = self.request.GET.get('radius', 0)

        # User specified not to get do location filter
        if all_bay_area and all_bay_area == 'Bay Area':
            if self.request.user.is_authenticated():
                profile = self.request.user.profile
                profile.last_filter_center = None
                profile.last_filter_radius = None
                profile.last_filter_location_name = ''
                profile.save()
            # Delete all location related cookies
            try:
                del self.request.session['latitude']
            except KeyError:
                pass
            try:
                del self.request.session['longitude']
            except KeyError:
                pass
            try:
                del self.request.session['radius']
            except KeyError:
                pass
            try:
                del self.request.session['location_name']
            except KeyError:
                pass
        # User provided new location filter info
        elif self.latitude and self.longitude and self.radius_mi:
            neighborhood = rev_geocode_location_component(self.latitude, self.longitude, 'neighborhood')
            if not neighborhood:
                #If not succeed in first try, try again (with a bigger net)
                neighborhood = rev_geocode_location_component(self.latitude, self.longitude, 'political')
            city = rev_geocode_location_component(self.latitude, self.longitude, 'locality')
            self.location_name = "{}, {}".format(neighborhood, city)
            if self.request.user.is_authenticated():
                profile = self.request.user.profile
                profile.last_filter_center = Point(self.longitude, self.latitude)
                profile.last_filter_radius = self.radius_mi
                profile.last_filter_location_name = self.location_name
                profile.save()
            # Set all location related cookies
            self.request.session['latitude'] = self.latitude
            self.request.session['longitude'] = self.longitude
            self.request.session['radius'] = self.radius_mi
            self.request.session['location_name'] = self.location_name
        # Check if this user already has last filter location stored
        elif self.request.user.is_authenticated() and self.request.user.profile.last_filter_center:
            self.latitude = self.request.user.profile.last_filter_center.y
            self.longitude = self.request.user.profile.last_filter_center.x
            self.radius_mi = self.request.user.profile.last_filter_radius
            self.location_name = self.request.user.profile.last_filter_location_name
        # Check if there is anything in the cookies to use
        else:
            self.latitude = self.request.session.get('latitude', None)
            self.longitude = self.request.session.get('longitude', None)
            self.radius_mi = self.request.session.get('radius', 7)
            self.location_name = self.request.session.get('location_name', '')

        self.category_slug = kwargs.get('cat_slug', None)
        self.category_list = Category.objects.filter(parent_category__isnull=False)

        return super(Events, self).get(request, *args, **kwargs)

    def get_queryset(self):
        er = EventsResource()
        request_bundle = er.build_bundle(request=self.request)
        queryset = er.obj_get_list(request_bundle).prefetch_related('category')

        # Apply any location filters if needed
        if self.latitude and self.longitude:
            origin = Point(self.longitude, self.latitude)
            self.radius_mi = self.radius_mi if self.radius_mi else 20
            queryset = queryset.filter(venue__point__distance_lt=(origin, D(mi=self.radius_mi))).\
                distance(origin, field_name='venue__point')
            self.location_available = True
        elif self.ordering == 'distance':
            # If an ordering by distance was requested but there is no location info, don't do the ordering
            self.ordering = ''

        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)
            try:
                self.category = Category.objects.get(slug=self.category_slug)
            except Category.DoesNotExist:
                pass

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

        context['now'] = timezone.now()
        context['events_list'] = json.loads(list_json)
        context['category_list'] = self.category_list
        context['category'] = self.category
        context['event_sort'] = self.ordering
        context['venue_radius'] = self.radius_mi
        context['page_template'] = self.page_template
        context['latitude'] = self.latitude
        context['longitude'] = self.longitude
        context['location_available'] = self.location_available
        context['location_string'] = self.location_name
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
        context['location_string'] = request.session.get('location_name', 'your location')
        return self.render_to_response(context)