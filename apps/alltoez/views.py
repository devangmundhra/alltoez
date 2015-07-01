import json

from django.http import HttpResponseServerError, HttpResponseRedirect, HttpResponse
from django.template import loader, RequestContext
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.paginator import InvalidPage, Paginator, EmptyPage, Page
from django.db.models import Max, Min
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.decorators import classonlymethod

from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from rest_framework.decorators import detail_route, renderer_classes, api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import keen

from apps.alltoez.graph.neo4j import get_similar_events
from apps.alltoez.serializers import EventSerializer, UserSerializer
from apps.events.models import Event, SimilarEvents
from apps.events.views import EventInternalViewSet

"""
ALLTOEZ API VIEWS
"""


class EventViewSet(EventInternalViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    serializer_class = EventSerializer

    def get_queryset(self):
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


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to use it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwner,)

@requires_csrf_token
def server_error(request, template_name='500.html'):
    """
    500 error handler.

    :param request:
    :param template_name:
    :return:
    """
    t = loader.get_template(template_name) # TODO: Create a 500.html template.
    return HttpResponseServerError(t.render(RequestContext(request, {'request_path': request.path})))

"""
Base alltoez views
"""


def home(request):
    """
    View to handle the default action when a user lands on a home page
    :param request: Request
    :return: relevant view depending on logged in status of user
    """
    if request.user.is_authenticated():
        return redirect('events')
    else:
        return render(request, "alltoez/home.html")


"""
Alltoez search views
"""


class AlltoezSearchView(FacetedSearchView):
    page_template = "alltoez/search/events_list_page.html"
    """
    AlltoezSearchView
    Search view for Alltoez
    """
    def get_query(self):
        query = super(AlltoezSearchView, self).get_query()
        keen.add_event('search', {
            "query": query
        }, timezone.now())
        return query

    def extra_context(self):
        extra = super(AlltoezSearchView, self).extra_context()
        if hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            extra['suggestion'] = self.form.get_suggestion()
        extra['page_template'] = self.page_template
        return extra

    def build_page(self):
        """
        Paginates the results appropriately.
        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        # start_offset = (page_no - 1) * self.results_per_page
        # self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except EmptyPage:
            page = None
        except InvalidPage:
            raise Http404("This is an invalid page number!")

        return (paginator, page)


def autocomplete(request):
    my_query = request.GET.get('q', '')
    sqs = SearchQuerySet().filter(end_date__gte=timezone.now().date()).autocomplete(title_auto=my_query)[:8]
    suggestions = [{'value': result.title} for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
