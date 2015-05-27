from rest_framework import viewsets

from apps.venues.serializers import VenueSerializer
from apps.venues.models import Venue

"""
API Endpoint for Venues module
"""


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows venues to be viewed or edited.
    """
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer