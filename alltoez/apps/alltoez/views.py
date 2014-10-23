from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template.defaulttags import regroup
from django.http import HttpResponseServerError
from django.template import loader, RequestContext
from django.conf import settings
from django.views.generic import TemplateView, FormView
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

from apps.alltoez.utils.view_utils import MessageMixin

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


class Home(TemplateView):
    template_name = "alltoez/home.html"

    def get_context_data(self, **kwargs):
        return {}

class Contact(TemplateView):
    template_name = "alltoez/contact.html"

    def get_context_data(self, **kwargs):
        return {}
