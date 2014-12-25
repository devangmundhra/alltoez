__author__ = 'devangmundhra'

from autocomplete_light import register
from apps.venues.models import Venue

# This will generate a VenueAutocomplete class
register(Venue,
    # Just like in ModelAdmin.search_fields
    search_fields=['name', 'address'],
    attrs={
        # This will set the input placeholder attribute:
        'placeholder': 'Venue name or address',
    },
    add_another_url_name='admin:venues_venue_add'
)
