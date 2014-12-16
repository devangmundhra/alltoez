from django.contrib import admin

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
    fields = ('name', 'phone_number', 'address', 'neighborhood',
              #('address', 'address_line_2', 'address_line_3'),
              #('city', 'state', 'country', 'postcode'),
              ('latitude', 'longitude'))
    search_fields = ['name', 'address']
    pass

admin.site.register(Venue, VenueAdmin)
