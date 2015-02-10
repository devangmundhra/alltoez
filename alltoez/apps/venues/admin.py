from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.venues.models import Venue


class VenueInline(admin.StackedInline):
    """
    Inline model form to edit event information
    Note: This is similar to VenueAdmin below
    """
    model = Venue
    exclude = ('slug',)
    max_num = 1
    extra = 1


class VenueAdmin(admin.ModelAdmin):
    """
    Model admin for Venue Model
    Note: This is similar to VenueInline above
    """
    fields = ('name', 'phone_number',
              ('address', 'address_line_2', 'address_line_3'),
              ('city', 'state', 'zipcode', 'country',),
              'neighborhood',
              'yelp_url', 'facebook_url', ('latitude', 'longitude'))
    search_fields = ['name', 'address']

admin.site.register(Venue, VenueAdmin)
