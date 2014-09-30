from django.conf.urls import url, patterns

from views import Home, Events, Contact
urlpatterns = patterns('',
	url(r"^$", Home.as_view(),  name="home"),
	url(r"^events/$", Events.as_view(),  name="events"),
	url(r"^contact/$", Contact.as_view(),  name="contact"),
)
