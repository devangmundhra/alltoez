from rest_framework import serializers
from allauth.socialaccount.models import SocialAccount

from apps.venues.api.serializers import VenueSerializer
from apps.events.api.serializers import EventSerializer


class VenueDetailSerializer(VenueSerializer):
    event_set = EventSerializer(many=True, read_only=True)

    class Meta(VenueSerializer.Meta):
        fields = VenueSerializer.Meta.fields + ('event_set',)


class AllauthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount