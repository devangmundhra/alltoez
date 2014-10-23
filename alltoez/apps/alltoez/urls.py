from django.conf.urls import url, patterns, include

from views import Home, Contact

urlpatterns = patterns('',
    url(r"^$", Home.as_view(),  name="home"),
    url(r"^events/", include('apps.events.urls')),
    url(r"^contact/$", Contact.as_view(),  name="contact"),
)
