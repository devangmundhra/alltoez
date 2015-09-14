from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.reverse import reverse
from sorl.thumbnail import get_thumbnail

from apps.events.models import Event, Category
from apps.user_actions.models import Bookmark, Done, Review
from apps.venues.serializers import VenueSerializer
from apps.user_actions.serializers import ReviewSerializer


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'description')


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
        if request.query_params.get('latitude', None) and request.query_params.get('longitude', None):
            origin = Point(float(request.query_params['longitude']), float(request.query_params['latitude']))
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


class TextSearchSerializer(serializers.ModelSerializer):
    # venue = VenueSerializer(read_only=True)
    description = serializers.CharField(read_only=True)
    min_age = serializers.IntegerField(read_only=True)
    max_age = serializers.IntegerField(read_only=True)
    cost = serializers.IntegerField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event
        fields = ( 'venue', 'title', 'description', 'min_age',
                  'max_age', 'cost', 'cost_detail','start_date','end_date'
                 )


class HaystackSerializer(serializers.Serializer):
    description = serializers.SerializerMethodField(method_name='_description')
    min_age = serializers.SerializerMethodField(method_name='_min_age')
    min_age = serializers.SerializerMethodField(method_name='_max_age')
    cost = serializers.SerializerMethodField(method_name='_cost')
    start_date = serializers.SerializerMethodField(method_name='_start_date')
    end_date = serializers.SerializerMethodField(method_name='_end_date')

    def _description(self, obj):
        return obj.object.description

    def _min_age(self, obj):
        return obj.object.min_age

    def _max_age(self, obj):
        return obj.object.min_age

    def _cost(self, obj):
        return obj.object.cost

    def _start_date(self, obj):
        return obj.object.start_date

    def _end_date(self, obj):
        return obj.object.end_date
