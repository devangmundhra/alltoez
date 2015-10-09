from django.utils import timezone
from django.db.models import Max, Min, Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.decorators import classonlymethod

import django_filters
from haystack.query import EmptySearchQuerySet

from rest_framework.decorators import detail_route, renderer_classes, api_view
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from apps.alltoez.serializers import EventSerializer
from apps.events.models import Event, Category
from apps.alltoez.graph.neo4j import get_similar_events
from apps.events.api.serializers import CategorySerializer, EventInternalSerializer,TextSearchSerializer, EventDetailSerializer
from apps.alltoez.serivces import EventSearchServices


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MultiFieldMethodFilter(django_filters.MethodFilter):
    """
    This filter will allow you to run a method that exists on the filterset class
    """
    def __init__(self, *args, **kwargs):
        self.fields = kwargs.get('fields', None)
        super(MultiFieldMethodFilter, self).__init__(*args, **kwargs)


class EventFilter(django_filters.FilterSet):
    min_age = django_filters.NumberFilter(name="min_age", lookup_type='gte')
    max_age = django_filters.NumberFilter(name="max_age", lookup_type='lte')
    category = django_filters.CharFilter(name="category__slug")
    max_cost = django_filters.NumberFilter(name="cost", lookup_type='lte')
    location = django_filters.MethodFilter(name="location", action='filter_location')

    class Meta:
        model = Event
        fields = ['category', 'min_age', 'max_age', 'max_cost', 'location']

    def filter_location(self, queryset, value):
        event_service = EventSearchServices(circle=value)
        qs = event_service.get_events_near_center(queryset)
        return qs

class EventInternalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventInternalSerializer
    ordering = ('-published_at',)
    ordering_fields = ('published_at', 'end_date', 'cost', 'min_age', 'max_age', 'view_count', 'distance')
    filter_class = EventFilter

    def get_queryset(self):
        qs = Event.objects.all().filter(publish=True).filter(Q(end_date__gte=timezone.now()) | Q(end_date=None))
        return qs


class EventViewSet(EventInternalViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        bounds = self.request.GET.get('bounds', None)
        zoom = self.request.GET.get('zoom', 8)
        qs = super(EventViewSet, self).get_queryset()
        if not self.request.user.is_authenticated():
            qs = qs.prefetch_related('category')
        else:
            # TODO: Use the current_age property instead of age here
            age_range = self.request.user.children.aggregate(Min('age'), Max('age'))
            min_age = age_range['age__min'] if age_range['age__min'] else Event.DEFAULT_MAX_AGE_EVENT #Yes, DEFAULT_MAX!
            max_age = age_range['age__max'] if age_range['age__max'] else Event.DEFAULT_MIN_AGE_EVENT #Yes, DEFAULT_MIN!
            # The above defaults are set in such a way so that no events are filtered unnecessarily
            qs = qs.filter(min_age__lte=min_age, max_age__gte=max_age).prefetch_related('category')
        event_service = EventSearchServices(zoom, bounds)
        if event_service.bounds:
            if self.request.user.is_authenticated():
                profile = self.request.user.profile
                profile.last_known_location_bounds = event_service.bounds
                profile.last_map_zoom = event_service.zoom
                profile.save()

            if not event_service.bounds and self.request.user.is_authenticated():
                event_service.bounds = self.request.user.profile.last_known_location_bounds
                event_service.zoom = self.request.user.profile.last_map_zoom

            qs = event_service.get_events_within_bounds(qs)

        return qs

    @detail_route(methods=['get'], renderer_classes=[TemplateHTMLRenderer])
    def similar(self, request, *args, **kwargs):
        template = "alltoez/recommendation/similar_events.html"
        if not request.is_ajax():
            return Response({"error": "This is not an ajax request"}, status=status.HTTP_400_BAD_REQUEST,
                            template_name=template)

        try:
            event = self.get_object()
        except ObjectDoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND, template_name=template)
        except MultipleObjectsReturned:
            return Response({"error": "More than one resource is found at this URI."},
                            status=status.HTTP_300_MULTIPLE_CHOICES, template_name=template)

        """
        THIS IS RECOMENDATION VIA PIO
        try:
            similar_event_map = SimilarEvents.objects.get(event=event)
            queryset = similar_event_map.similar_events.all().filter(Q(end_date__gte=timezone.now().date()) |
                                                                     Q(end_date=None)).order_by('?')[:3]
        except ObjectDoesNotExist:
            queryset = Event.objects.none()
        """
        queryset = get_similar_events(event=event, limit=3, skip=0)
        serializer = self.get_serializer(queryset, many=True)

        return Response({"events_list": serializer.data}, template_name=template)

    @classonlymethod
    def get_direct_queryset(cls, request, **initkwargs):
        """
        TODO: Temporary until a better way is found
        """
        self = cls(**initkwargs)
        request = Request(request, authenticators=(BasicAuthentication(), SessionAuthentication()))
        self.request = request

        return self.get_queryset()


class EventDetailViewSet(viewsets.ModelViewSet):

    serializer_class = EventDetailSerializer
    http_method_names = ['get']

    def get_queryset(self,*args,**kwargs):
        request = self.request

        if request.GET.get('q') is not None:
            query = request.GET.get('q')
            queryset = Event.objects.filter(id = query)
            return queryset

        else:
            queryset = []
            return queryset

