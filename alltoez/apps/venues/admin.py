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


class UnFormattedVenueListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Unprocessed Venues')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'raw_address'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('unprocessed', _('unprocessed venues')),
            ('processed', _('processed venues'))
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'unprocessed':
            return queryset.filter(raw_address__isnull=True)
        if self.value() == 'processed':
            return queryset.filter(raw_address__isnull=False)


class VenueAdmin(admin.ModelAdmin):
    """
    Model admin for Venue Model
    Note: This is similar to VenueInline above
    """
    fields = ('name', 'phone_number',
              ('address', 'address_line_2', 'address_line_3'),
              ('city', 'state', 'country', 'zipcode'),
              'neighborhood',
              'yelp_url', 'facebook_url', ('latitude', 'longitude'))
    search_fields = ['name', 'address']
    list_filter = (UnFormattedVenueListFilter,)
    pass

admin.site.register(Venue, VenueAdmin)
