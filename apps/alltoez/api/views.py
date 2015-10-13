from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from apps.events.api.serializers import EventSerializer
from apps.alltoez_profile.api.serializers import UserSerializer
from apps.user_actions.models import Bookmark, Done
from apps.events.models import Event


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to use it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwner,)

    @list_route(methods=['get'],)
    def me(self, request):
        user = request.user
        if not user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = self.get_serializer(user)
            return Response(serializer.data)

    @detail_route(methods=['get'])
    def bookmarked(self, request, pk=None):
        user = self.get_object()
        bookmarked_events = Event.objects.none()
        if user.is_authenticated():
            bookmarked_event_ids = Bookmark.objects.filter(user=user).prefetch_related('event').\
                values_list('event__id', flat=True)
            bookmarked_events = Event.objects.filter(pk__in=bookmarked_event_ids)
        serializer = EventSerializer(bookmarked_events, many=True, context=request.parser_context)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def done(self, request, pk=None):
        user = self.get_object()
        done_events = Event.objects.none()
        if user.is_authenticated():
            done_event_ids = Done.objects.filter(user=user).prefetch_related('event').\
                values_list('event__id', flat=True)
            done_events = Event.objects.filter(pk__in=done_event_ids)
        serializer = EventSerializer(done_events, many=True, context=request.parser_context)
        return Response(serializer.data)
