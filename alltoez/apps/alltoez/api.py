import json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Max, Min
from django.conf.urls import url
from django.shortcuts import render_to_response
from django.template import RequestContext

from tastypie.utils import trailing_slash
from tastypie import fields
from tastypie.http import HttpGone, HttpMultipleChoices, HttpBadRequest

from apps.events.api import EventInternalResource
from apps.alltoez_profile.api import AlltoezProfileInternalResource
from apps.user_actions.models import Bookmark, Done
from apps.user_actions.api import BookmarkResource, DoneResource
from apps.events.models import Event
from apps.alltoez.ml.pio_data import get_similar_events


class EventsResource(EventInternalResource):
    """
    EventResource
    This is the actual resource that is exposed by the API
    """
    bookmark = fields.CharField(attribute='bookmark', null=True, blank=True)
    done = fields.ToOneField(DoneResource, attribute='done', null=True, blank=True)

    class Meta(EventInternalResource.Meta):
        # resource_name = 'events'
        # Note that the resource name is same as EventInternalResource, so there are 2 resources with the same names.
        # This is necessary because while the events exposed are through this resource (EventsResource), the user
        # actions API (like done, bookmark) uses the EventInternalResource. So the public will have a pointer to the
        # resource_uri for EventsResource, but when calling a bookmark/done they would need a resource_uri for
        # EventInternalResource. This is a small hack so that both EventsResource and EventsInternalResource have
        # the same resource_uri, but only one of them is exposed.
        pass

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/similar/(?P<pk>\w[\w/-]*)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_recommendations'), name="api_get_recommendations"),
        ]

    def get_recommendations(self, request, **kwargs):
        template = "alltoez/recommendation/similar_events.html"

        if not request.is_ajax():
            return HttpBadRequest("This is not an ajax request")

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        try:
            bundle = self.build_bundle(data={'pk': kwargs['pk']}, request=request)
            event = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        object_ids = get_similar_events(event)

        er = EventsResource()
        queryset = Event.objects.filter(pk__in=object_ids)

        bundles = []
        for obj in queryset:
            bundle = er.build_bundle(obj=obj, request=request)
            bundles.append(er.full_dehydrate(bundle, for_list=True))

        list_json = er.serialize(None, bundles, "application/json")
        objects = json.loads(list_json)

        self.log_throttled_access(request)
        return render_to_response(template,
                                  {"events_list": objects},
                                  context_instance=RequestContext(request))

    def dehydrate_bookmark(self, bundle):
        if not bundle.request.user.is_authenticated():
            return None
        try:
            bookmark = Bookmark.objects.get(event=bundle.obj, user=bundle.request.user)
            bm_resource = BookmarkResource()
            return bm_resource.get_resource_uri(bookmark)
        except ObjectDoesNotExist:
            return None

    def dehydrate_done(self, bundle):
        if not bundle.request.user.is_authenticated():
            return None
        try:
            done = Done.objects.get(event=bundle.obj, user=bundle.request.user)
            dn_resource = DoneResource()
            return dn_resource.get_resource_uri(done)
        except ObjectDoesNotExist:
            return None

    def get_object_list(self, request):
        """
        Filters the object list based on the ages of the user's children
        :param request:
        :return: Queryset of events for the user
        """
        # If user is not authenticated, show all the events
        orig_events_list = super(EventsResource, self).get_object_list(request)
        if not request.user.is_authenticated():
            return orig_events_list
        else:
            # TODO: Use the current_age property instead of age here
            age_range = request.user.children.aggregate(Min('age'), Max('age'))
            min_age = age_range['age__min'] if age_range['age__min'] else Event.DEFAULT_MAX_AGE_EVENT #Yes, DEFAULT_MAX!
            max_age = age_range['age__max'] if age_range['age__max'] else Event.DEFAULT_MIN_AGE_EVENT #Yes, DEFAULT_MIN!
            # The above defaults are set in such a way so that no events are filtered unnecessarily
            return orig_events_list.filter(min_age__lte=min_age, max_age__gte=max_age)


class AlltoezProfileResource(AlltoezProfileInternalResource):
    """
    AlltoezProfileResource
    This is the actual resource that is exposed by the API
    """
    bookmarked_events = fields.ToManyField(EventsResource, 'bookmarked_events', blank=True, null=True)
    done_events = fields.ToManyField(EventsResource, 'done_events', blank=True, null=True)

    class Meta(AlltoezProfileInternalResource.Meta):
        # resource_name = 'users'
        pass

    def dehydrate_bookmarked_events(self, bundle):
        profile = bundle.obj
        user = profile.user
        bookmarked_event_ids = Bookmark.objects.filter(user=user).prefetch_related('event').\
            values_list('event__id', flat=True)
        bookmarked_events = Event.objects.filter(pk__in=bookmarked_event_ids)
        dehydrated_events = []
        for event in bookmarked_events:
            er = EventsResource()
            er_bundle = er.build_bundle(obj=event, request=bundle.request)
            event_dict = er.full_dehydrate(er_bundle).data
            dehydrated_events.append(event_dict)
        return dehydrated_events

    def dehydrate_done_events(self, bundle):
        profile = bundle.obj
        user = profile.user
        done_event_ids = Done.objects.filter(user=user).prefetch_related('event').\
            values_list('event__id', flat=True)
        done_events = Event.objects.filter(pk__in=done_event_ids)
        dehydrated_events = []
        for event in done_events:
            er = EventsResource()
            er_bundle = er.build_bundle(obj=event, request=bundle.request)
            event_dict = er.full_dehydrate(er_bundle).data
            dehydrated_events.append(event_dict)
        return dehydrated_events