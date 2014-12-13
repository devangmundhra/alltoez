from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Min, Q

from tastypie import fields

from apps.events.api import EventInternalResource
from apps.user_actions.models import Bookmark, Done
from apps.user_actions.api import BookmarkResource, DoneResource
from apps.events.models import Event


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
        orig_events_list = super(EventsResource, self).get_object_list(request).filter(
            Q(end_date__gte=timezone.now().date()) | Q(end_date=None)).order_by('-created_at')
        if not request.user.is_authenticated():
            return orig_events_list
        else:
            age_range = request.user.children.aggregate(Min('age'), Max('age'))
            min_age = age_range['age__min'] if age_range['age__min'] else Event.DEFAULT_MAX_AGE_EVENT #Yes, DEFAULT_MAX!
            max_age = age_range['age__max'] if age_range['age__max'] else Event.DEFAULT_MIN_AGE_EVENT #Yes, DEFAULT_MIN!
            # The above defaults are set in such a way so that no events are filtered unnecessarily
            return orig_events_list.filter(min_age__lte=min_age, max_age__gte=max_age)

