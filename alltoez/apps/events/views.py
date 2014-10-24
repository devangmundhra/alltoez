from datetime import datetime, date

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.http import Http404
from django.utils import timezone
from django.db.models import Q

from apps.events.models import Event, Category


class Events(ListView):
    template_name = "events.html"
    model = Event
    events_list = None
    category = None
    category_list = None
    category_slug = None

    def get(self, request, *args, **kwargs):
        sort = self.request.GET.get('sort')
        self.category_slug = kwargs.get('slug', None)

        self.category_list = Category.objects.filter(parent_category__isnull=False)
        # Note: -created_at is also the default option for sorting in events.html template
        self.events_list = Event.objects.filter(Q(end_date__gte=timezone.now().date()) | Q(end_date=None)).order_by('-created_at')
        if self.category_slug:
            self.events_list = self.events_list.filter(category__slug=self.category_slug)
            try:
                self.category = Category.objects.get(slug=self.category_slug)
            except Category.DoesNotExist:
                pass
        if sort:
            self.events_list = self.events_list.order_by(sort)
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
    template_name = 'event_detail.html'
