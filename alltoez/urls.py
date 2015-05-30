from django.conf.urls import url, patterns, include
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

from filebrowser.sites import site

handler500 = 'apps.alltoez.views.server_error'

# Pluggable / django apps / inernal apps
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.alltoez.urls')),
    url(r'^events/', include('apps.events.urls')),
    url(r'^accounts/', include('apps.alltoez_profile.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

urlpatterns += patterns('',
	url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'ico/favicon.ico', permanent=True)),
	url(r'^apple\-touch\-icon\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'img/apple-touch-icon.png',
                                                           permanent=True)),
	url(r'^robots\.txt$', RedirectView.as_view(url=settings.STATIC_URL + 'robots.txt', permanent=True))
)

if settings.DEBUG:
	urlpatterns+= patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.MEDIA_ROOT
		}),
		(r'^cache-forever/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.STATIC_ROOT,
		}),
		(r'^404/$', 'django.views.defaults.page_not_found'),
		(r'^500/$', 'apps.alltoez.views.server_error')
	)

urlpatterns += staticfiles_urlpatterns()