from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.events.models import Event
from apps.user_actions.models import Bookmark, Done
from apps.alltoez_profile.serializers import UserInternalSerializer
from apps.events.serializers import EventInternalSerializer


class EventSerializer(EventInternalSerializer):
    bookmark = serializers.SerializerMethodField(read_only=True)
    done = serializers.SerializerMethodField(read_only=True)

    class Meta(EventInternalSerializer.Meta):
        fields = EventInternalSerializer.Meta.fields + ('bookmark', 'done')

    def get_bookmark(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated():
            return None
        try:
            bookmark = Bookmark.objects.get(event=obj, user=request.user)
            return reverse('api:bookmark-detail', args=(bookmark,), request=request)
        except ObjectDoesNotExist:
            return None

    def get_done(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated():
            return None
        try:
            done = Done.objects.get(event=obj, user=request.user)
            return reverse('api:done-detail', args=(done,), request=request)
        except ObjectDoesNotExist:
            return None


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