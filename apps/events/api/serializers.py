from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.reverse import reverse
from sorl.thumbnail import get_thumbnail
from drf_haystack.serializers import HaystackSerializerMixin

from apps.events.models import Event, Category
from apps.user_actions.models import Bookmark, Done, Review
from apps.venues.api.serializers import VenueSerializer
from apps.user_actions.api.serializers import ReviewSerializer
from apps.events.search_indexes import EventIndex

class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'font_awesome_icon_class')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    parent_category = ParentCategorySerializer()

    class Meta:
        model = Category
        fields = ('name', 'slug', 'description', 'font_awesome_icon_class', 'parent_category')


class EventInternalSerializer(serializers.HyperlinkedModelSerializer):
    distance = serializers.SerializerMethodField()
    venue = VenueSerializer(read_only=True)
    category = CategorySerializer(many=True)
    thumbnail_384_256 = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('pk', 'id', 'created_at', 'updated_at', 'venue', 'title', 'slug', 'description', 'category', 'image', 'min_age',
                  'max_age', 'cost', 'cost_detail', 'start_date', 'end_date', 'recurrence_detail', 'time_detail', 'url',
                  'additional_info', 'published_at', 'distance', 'thumbnail_384_256')

    def get_distance(self, obj):
        request = self.context.get('request')
        origin = None
        if request.GET.get('latitude', None) and request.GET.get('longitude', None):
            origin = Point(float(request.GET['longitude']), float(request.GET['latitude']))
        elif request.user.is_authenticated() and request.user.profile.last_known_location_bounds:
            lat = request.user.profile.last_known_location_bounds.centroid.y
            lng = request.user.profile.last_known_location_bounds.centroid.x
            origin = Point(lng, lat)
        if not origin:
            return None
        event = Event.objects.all().filter(id=obj.id).distance(origin, field_name='venue__point').first()
        dObj = event.distance
        if dObj is not None:
            return dObj.mi
        return None

    def get_thumbnail_384_256(self, obj):
        try:
            im = get_thumbnail(obj.image, '384x256', crop='center')
            url = im.url
            request = self.context.get('request', None)
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        except (ValueError, IOError):
            return None


class EventSerializer(EventInternalSerializer):
    bookmark = serializers.SerializerMethodField(read_only=True)
    done = serializers.SerializerMethodField(read_only=True)
    review = serializers.SerializerMethodField(read_only=True, required=False)
    view_count = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta(EventInternalSerializer.Meta):
        fields = EventInternalSerializer.Meta.fields + ('bookmark', 'done', 'review', 'view_count')

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

    def get_review(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated():
            return None
        try:
            review = Review.objects.get(event=obj, user=request.user)
            serializer = ReviewSerializer(review, context=self.context)
            return serializer.data
        except ObjectDoesNotExist:
            return None

    def get_view_count(self, obj):
        return obj.view_seed + obj.viewip_set.count()


class EventSearchSerializer(HaystackSerializerMixin, EventSerializer):
    class Meta(EventSerializer.Meta):
        index_classes = [EventIndex, ]

        search_fields = ('text',)
