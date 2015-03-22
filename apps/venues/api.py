__author__ = 'devangmundhra'

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.cache import SimpleCache

from apps.venues.models import Venue


class VenueInternalResource(ModelResource):
    """
    Internal resource not directly exposed by the api
    """
    phone_number = fields.CharField(attribute='phone_number', null=True, blank=True)

    class Meta:
        queryset = Venue.objects.all()
        resource_name = 'venues'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        includes = ['name', 'full_address', 'location', 'phone_number', 'neighborhood']
        cache = SimpleCache(timeout=10)

    def dehydrate_address(self, bundle):
        return bundle.obj.display_address()

    def dehydrate_phone_number(self, bundle):
        phone_number = bundle.obj.phone_number
        if phone_number:
            phone_number = phone_number.as_national
        return phone_number