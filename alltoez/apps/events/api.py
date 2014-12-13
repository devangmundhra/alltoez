from tastypie.resources import ModelResource
from tastypie import fields

from apps.events.models import Event


class EventInternalResource(ModelResource):
    """
    Internal resource not directly exposed by the api
    This resource is exposed via the EventResource in apps.user_actions.api
    """
    image = fields.DictField(attribute='image')
    phone_number = fields.CharField(attribute='phone_number', null=True, blank=True)

    class Meta:
        queryset = Event.objects.all()
        resource_name = 'events'

    def dehydrate_phone_number(self, bundle):
        phone_number = bundle.obj.phone_number
        if phone_number:
            phone_number = phone_number.as_national
        return phone_number