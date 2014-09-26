from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

from apps.alltoez.utils.view_utils import MessageMixin

@requires_csrf_token
def server_error(request, template_name='500.html'):
	"""
	500 error handler.

	Templates: `500.html`
	Context: None
	"""
	t = loader.get_template(template_name) # You need to create a 500.html template.
	return http.HttpResponseServerError(t.render(RequestContext(request, {'request_path': request.path, 'STATIC_URL':settings.STATIC_URL, 'MEDIA_URL':settings.MEDIA_URL})))

"""
Base alltoez views
"""
class Home(TemplateView):
	template_name = "alltoez/home.html"

	def get_context_data(self, **kwargs):
		return {}
