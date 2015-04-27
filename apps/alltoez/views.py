import json

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template.defaulttags import regroup
from django.http import HttpResponseServerError, HttpResponseRedirect, HttpResponse
from django.template import loader, RequestContext
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.shortcuts import render, redirect
from django.utils import timezone

from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet

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
    def extra_context(self):
        extra = super(AlltoezSearchView, self).extra_context()
        if hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            extra['suggestion'] = self.form.get_suggestion()
        extra['page_template'] = self.page_template
        return extra

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
