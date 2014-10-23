from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

from filebrowser.sites import site
import os

handler500 = 'apps.alltoez.views.server_error'
admin.autodiscover()

# Pluggable / django apps / inernal apps
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.alltoez.urls')),
    url(r'^accounts/', include('apps.alltoez_profile.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^summernote/', include('django_summernote.urls')),
)

urlpatterns += patterns('',
	url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
	url(r'^apple\-touch\-icon\.png$', RedirectView.as_view(url='/static/img/apple-touch-icon.png')),
	url(r'^robots\.txt$', RedirectView.as_view(url='/static/robots.txt'))
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
