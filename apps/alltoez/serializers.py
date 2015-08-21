import json

from rest_framework import serializers

from apps.events.models import Event
from apps.user_actions.models import Bookmark, Done
from apps.alltoez_profile.serializers import UserInternalSerializer
from apps.venues.serializers import VenueSerializer
from apps.events.api.serializers import EventSerializer
from allauth.socialaccount.models import SocialAccount


class UserSerializer(UserInternalSerializer):
    bookmarked_events = serializers.SerializerMethodField(read_only=True, required=False)
    done_events = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta(UserInternalSerializer.Meta):
        fields = UserInternalSerializer.Meta.fields + ('bookmarked_events', 'done_events')

    def get_bookmarked_events(self, obj):
        if not obj.is_authenticated():
            return None
        bookmarked_event_ids = Bookmark.objects.filter(user=obj).prefetch_related('event').\
            values_list('event__id', flat=True)
        bookmarked_events = Event.objects.filter(pk__in=bookmarked_event_ids)
        serializer = EventSerializer(bookmarked_events, many=True, context=self.context)
        return serializer.data

    def get_done_events(self, obj):
        if not obj.is_authenticated():
            return None
        done_event_ids = Done.objects.filter(user=obj).prefetch_related('event').\
            values_list('event__id', flat=True)
        done_events = Event.objects.filter(pk__in=done_event_ids)
        serializer = EventSerializer(done_events, many=True, context=self.context)
        return serializer.data


class VenueDetailSerializer(VenueSerializer):
    event_set = EventSerializer(many=True, read_only=True)

    class Meta(VenueSerializer.Meta):
        fields = VenueSerializer.Meta.fields + ('event_set',)

class AllauthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount