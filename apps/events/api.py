from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from django.contrib.gis.geos import Point

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.cache import SimpleCache
import newrelic.agent

from apps.events.models import Event, Category
from apps.venues.api import VenueInternalResource


class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        fields = ['name', 'slug', 'description']


class EventInternalResource(ModelResource):
    """
    Internal resource not directly exposed by the api
    This resource is exposed via the EventResource in apps.alltoez.api
    """
    image = fields.FileField(attribute='image')
    venue = fields.ForeignKey(VenueInternalResource, 'venue', full=True)
    category = fields.ToManyField(CategoryResource, attribute='category', full=True)
    distance = fields.DecimalField(blank=True, null=True)

    class Meta:
        queryset = Event.objects.all()
        resource_name = 'events'
        cache = SimpleCache(timeout=10)

    @newrelic.agent.function_trace()
    def get_object_list(self, request):
        """
        Filters the object list based on end date
        :param request:
        :return: Queryset of events
        """
        # If user is not authenticated, show all the events
        return super(EventInternalResource, self).get_object_list(request).filter(publish=True).filter(
            Q(end_date__gte=timezone.now()) | Q(end_date=None)).order_by('-published_at')

    @newrelic.agent.function_trace()
    def dehydrate_distance(self, bundle):
        origin = None
        if bundle.request.user.is_authenticated() and bundle.request.user.profile.last_filter_center:
            lat = bundle.request.user.profile.last_filter_center.y
            lng = bundle.request.user.profile.last_filter_center.x
        # Check if there is anything in the cookies to use
        else:
            lat = bundle.request.session.get('latitude', None)
            lng = bundle.request.session.get('longitude', None)

        if lat and lng:
            origin = Point(lng, lat)
        if not origin:
            return None
        event = Event.objects.all().filter(id=bundle.obj.id).distance(origin, field_name='venue__point').first()
        dObj = event.distance
        if dObj is not None:
            return dObj.mi
        return None