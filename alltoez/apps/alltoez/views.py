from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template.defaulttags import regroup
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.template import loader, RequestContext
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.shortcuts import render, redirect

from haystack.views import FacetedSearchView


@requires_csrf_token
def server_error(request, template_name='500.html'):
    """
    500 error handler.

    :param request:
    :param template_name:
    :return:
    """
    t = loader.get_template(template_name) # TODO: Create a 500.html template.
    return HttpResponseServerError(t.render(RequestContext(request, {'request_path': request.path,
                                                                     'STATIC_URL': settings.STATIC_URL,
                                                                     'MEDIA_URL': settings.MEDIA_URL})))

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


class Home(TemplateView):
    template_name = "alltoez/home.html"

    def get_context_data(self, **kwargs):
        return {}


class Contact(TemplateView):
    template_name = "alltoez/contact.html"

    def get_context_data(self, **kwargs):
        return {}


class AlltoezSearchView(FacetedSearchView):
    page_template = "alltoez/search/events_list_page.html"
    """
    AlltoezSearchView
    Search view for Alltoez
    """
    def extra_context(self):
        extra = super(AlltoezSearchView, self).extra_context()
        extra['page_template'] = self.page_template
        return extra