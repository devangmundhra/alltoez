from datetime import datetime, date

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template.defaulttags import regroup
from django.http import Http404, HttpResponseServerError, HttpResponseBadRequest
from django.template import loader, RequestContext
from django.conf import settings
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.utils import timezone

from apps.alltoez.utils.view_utils import MessageMixin
from apps.events.models import Event, Category, EventRecord

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


class EventRecords(ListView):
    template_name = "alltoez/events.html"
    model = EventRecord
    event_records_list = None
    category = None
    category_list = None
    category_slug = None

    def get(self, request, *args, **kwargs):
        sort = self.request.GET.get('sort')
        self.category_slug = kwargs.get('slug', None)

        self.category_list = Category.objects.filter(parent_category__isnull=False)
        self.event_records_list = EventRecord.objects.filter(date__gt=timezone.now().date()).order_by('date')
        if self.category_slug:
            self.event_records_list = self.event_records_list.filter(event__category__slug=self.category_slug)
            try:
                self.category = Category.objects.get(slug=self.category_slug)
            except Category.DoesNotExist:
                pass
        if sort:
            sort = 'event__'+sort
            self.event_records_list = self.event_records_list.order_by(sort)
        return super(EventRecords, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventRecords, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['event_records_list'] = self.event_records_list
        context['category_list'] = self.category_list
        context['category'] = self.category
        return context


# class EventsFragmentListView(ListView):
#     template_name = "alltoez/ui/fragments/events_list.html"
#     model = Event
#     events_list = None
#
#     def get(self, request, *args, **kwargs):
#         sort = self.request.GET.get('sort')
#         # order by whatever
#         if not sort:
#             return HttpResponseBadRequest()
#
#         if category_slug:
#             self.events_list = Event.objects.filter(category=category_slug)
#         else:
#             self.events_list = Event.objects.filter(category=category_slug)
#
#         if sort == 'all':
#             self.events_list = Event.objects.all()
#         self.events_list = Event.objects.all().order_by(sort)
#         return super(EventsFragmentListView, self).get(self, request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(EventsFragmentListView, self).get_context_data(**kwargs)
#         context = {
#             'events_list': self.events_list
#         }
#         return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'alltoez/event_detail.html'
    event_record = None

    def get(self, request, *args, **kwargs):
        datestr = self.request.GET.get('date')
        event = self.get_object()
        if datestr:
            ev_date = datetime.strptime(datestr, "%b%d %y").date()
            try:
                self.event_record = EventRecord.objects.get(event=event, date=ev_date)
            except EventRecord.DoesNotExist:
                self.event_record = None

        if not self.event_record:
            # Get the first event record for this object
            self.event_record = EventRecord.objects.filter(event=event, date__gt=datetime.now().date()).first()

        if not self.event_record:
            raise Http404(u"We don't have this event scheduled in the near future. Please check back later.")

        return super(EventDetailView, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context['event_record'] = self.event_record
        return context

class Contact(TemplateView):
    template_name = "alltoez/contact.html"

    def get_context_data(self, **kwargs):
        return {}
