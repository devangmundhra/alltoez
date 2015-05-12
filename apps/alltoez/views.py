import json

from django.http import HttpResponseServerError, HttpResponseRedirect, HttpResponse
from django.template import loader, RequestContext
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.paginator import InvalidPage, Paginator, EmptyPage, Page

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

    def build_page(self):
        """
        Paginates the results appropriately.
        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        # start_offset = (page_no - 1) * self.results_per_page
        # self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except EmptyPage:
            page = None
        except InvalidPage:
            raise Http404("This is an invalid page number!")

        return (paginator, page)


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
