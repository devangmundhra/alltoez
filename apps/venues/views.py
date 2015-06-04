import json

from django.views.generic import DetailView

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

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


class VenueDetailView(DetailView):
    model = Venue
    template_name = 'venues/venue_detail.html'
    object = None
    page_template = 'events/event_list_page.html'
    request = None

    def get_context_data(self, **kwargs):
        from apps.alltoez.serializers import VenueDetailSerializer
        context = super(VenueDetailView, self).get_context_data(**kwargs)
        serializer = VenueDetailSerializer(self.object, context={'request': self.request})
        venue_json = JSONRenderer().render(serializer.data)
        venue = json.loads(venue_json)
        context['venue'] = venue
        context['page_template'] = self.page_template
        return context
