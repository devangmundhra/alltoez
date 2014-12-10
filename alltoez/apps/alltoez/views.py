import json

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template.defaulttags import regroup
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.template import loader, RequestContext
from django.conf import settings
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.utils import timezone
from django.shortcuts import render, redirect

from endless_pagination.views import AjaxListView

from apps.events.models import Event, Category
from apps.alltoez.api import EventsResource

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


"""
Alltoez feed views
"""


class Events(AjaxListView):
    template_name = 'alltoez/events/events.html'
    page_template="alltoez/events/event_list_page.html"
    model = Event
    events_list = None
    category = None
    category_list = None
    category_slug = None

    def get(self, request, *args, **kwargs):
        sort = self.request.GET.get('sort')
        self.category_slug = kwargs.get('cat_slug', None)
        self.category_list = Category.objects.filter(parent_category__isnull=False)

        er = EventsResource()
        request_bundle = er.build_bundle(request=request)
        queryset = er.obj_get_list(request_bundle)

        # Note: -created_at is also the default option for sorting in events.html template
        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)
            try:
                self.category = Category.objects.get(slug=self.category_slug)
            except Category.DoesNotExist:
                pass
        if sort:
            queryset = queryset.order_by(sort)
        bundles = []
        for obj in queryset:
            bundle = er.build_bundle(obj=obj, request=request)
            bundles.append(er.full_dehydrate(bundle, for_list=True))

        list_json = er.serialize(None, bundles, "application/json")
        self.events_list = json.loads(list_json)
        return super(Events, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Events, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['events_list'] = self.events_list
        context['category_list'] = self.category_list
        context['category'] = self.category
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'alltoez/events/event_detail.html'
    object = None

    def get(self, request, *args, **kwargs):
        """
        This method has been copied from django/views/generic/detail.py
        :param request:
        :param args:
        :param kwargs:
        :return: HttpResponse
        """
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        er = EventsResource()
        er_bundle = er.build_bundle(obj=self.object, request=request)
        event_json = er.serialize(None, er.full_dehydrate(er_bundle), 'application/json')
        event = json.loads(event_json)
        context['event'] = event
        context['event_json'] = event_json
        return self.render_to_response(context)