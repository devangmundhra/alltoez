from django.core.exceptions import ObjectDoesNotExist
from tastypie import fields

from apps.events.api import EventInternalResource
from apps.user_actions.models import Bookmark, Done
from apps.user_actions.api import BookmarkResource, DoneResource


class EventsResource(EventInternalResource):
    """
    EventResource
    This is the actual resource that is exposed by the API
    """
    bookmark = fields.CharField(attribute='bookmark', null=True, blank=True)
    done = fields.ToOneField(DoneResource, attribute='done', null=True, blank=True)

    class Meta(EventInternalResource.Meta):
        resource_name = 'events'

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


