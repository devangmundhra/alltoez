from django.conf.urls import url, patterns

from apps.events.views import Events, EventDetailView

urlpatterns = patterns('',
    url(r"^$", Events.as_view(page_template="event_list_page.html"), {'slug': None}, name="events"),
    url(r"^(?P<slug>[\w-]+)/$", Events.as_view(page_template="event_list_page.html"), name="events"),
    url(r"^san-francisco/(?P<slug>[\w-]+)/$", EventDetailView.as_view(), name="event_detail"),
)
