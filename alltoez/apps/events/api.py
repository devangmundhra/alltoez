from tastypie.resources import ModelResource
from tastypie import fields

from apps.events.models import Event
from apps.venues.api import VenueInternalResource


class EventInternalResource(ModelResource):
    """
    Internal resource not directly exposed by the api
    This resource is exposed via the EventResource in apps.user_actions.api
    """
    image = fields.DictField(attribute='image')
    venue = fields.ForeignKey(VenueInternalResource, 'venue', full=True)

    class Meta:
        queryset = Event.objects.all()
        resource_name = 'events'