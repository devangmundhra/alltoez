from django.contrib.gis.geos import Point

from rest_framework import serializers

from apps.events.models import Event, Category
from apps.venues.serializers import VenueSerializer


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'description')


class EventInternalSerializer(serializers.HyperlinkedModelSerializer):
    distance = serializers.SerializerMethodField()
    venue = VenueSerializer(read_only=True)
    category = CategorySerializer(many=True)

    class Meta:
        model = Event
        fields = ('pk', 'id', 'created_at', 'updated_at', 'venue', 'title', 'slug', 'description', 'category', 'image', 'min_age',
                  'max_age', 'cost', 'cost_detail', 'start_date', 'end_date', 'recurrence_detail', 'time_detail', 'url',
                  'additional_info', 'published_at', 'distance')

    def get_distance(self, obj):
        request = self.context.get('request')
        origin = None
        if request.user.is_authenticated() and request.user.profile.last_filter_center:
            lat = request.user.profile.last_filter_center.y
            lng = request.user.profile.last_filter_center.x
        # Check if there is anything in the cookies to use
        else:
            lat = request.session.get('latitude', None)
            lng = request.session.get('longitude', None)

        if lat and lng:
            origin = Point(lng, lat)
        if not origin:
            return None
        event = Event.objects.all().filter(id=obj.id).distance(origin, field_name='venue__point').first()
        dObj = event.distance
        if dObj is not None:
            return dObj.mi
        return None