from django.db.models import Q
from django.utils import timezone

from tastypie.resources import ModelResource
from tastypie import fields

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
    image = fields.DictField(attribute='image')
    venue = fields.ForeignKey(VenueInternalResource, 'venue', full=True)
    category = fields.ToManyField(CategoryResource, attribute='category', full=True)

    class Meta:
        queryset = Event.objects.all()
        resource_name = 'events'

    def get_object_list(self, request):
        """
        Filters the object list based on end date
        :param request:
        :return: Queryset of events
        """
        # If user is not authenticated, show all the events
        return super(EventInternalResource, self).get_object_list(request).filter(
            Q(end_date__gte=timezone.now().date()) | Q(end_date=None)).order_by('-created_at')