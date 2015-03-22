from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from django.core import urlresolvers
from django.contrib.sites.models import Site

# from pagedown.widgets import AdminPagedownWidget
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from apps.events.models import DraftEvent, Event, EventRecord, Category


class ExpiredEventListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Event Expiry')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'end_date'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('unexpired', _('non-expired events')),
            ('expired', _('expired events')),
            ('no_expiry', _('events with no end date'))
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'unexpired':
            return queryset.filter(Q(end_date__gte=timezone.now().date()) | Q(end_date=None))
        if self.value() == 'expired':
            return queryset.filter(end_date__lt=timezone.now().date())
        if self.value() == 'no_expiry':
            return queryset.filter(Q(end_date=None))


class PublishedEventListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Event Published')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'publish'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('unpublished', _('unpublished events')),
            ('published', _('published events'))
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'unpublished':
            return queryset.filter(publish=False)
        if self.value() == 'published':
            return queryset.filter(publish=True)


class EventAdminForm(forms.ModelForm):
    """
    Custom form for event admin form
    """

    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        # self.fields['description'].widget = AdminPagedownWidget()
        # self.fields['time_detail'].widget = AdminPagedownWidget()
        # self.fields['additional_info'].widget = AdminPagedownWidget()

    def clean(self):
        end_date = self.cleaned_data.get('end_date', None)
        recurrence_detail = self.cleaned_data.get('recurrence_detail', None)

        if not end_date and not recurrence_detail:
            raise forms.ValidationError("Please add either an end date or recurrence detail for the event",
                                        code="incorrect")

        return self.cleaned_data

    def clean_venue(self):
        venue = self.cleaned_data.get('venue', None)
        if not venue:
            raise forms.ValidationError("An entry for venue is missing", code="incorrect")

        return venue


class EventInline(admin.StackedInline):
    """
    Inline model form to edit event information
    Note: This is similar to EventAdmin below
    """
    model = Event
    exclude = ('slug',)
    max_num = 1
    extra = 1
    related_search_fields = {
        'venue': ('name', 'address'),
    }
    form = EventAdminForm


class DraftEventAdminForm(forms.ModelForm):
    """
    Custom form for DraftEvent admin form
    """
    def __init__(self, *args, **kwargs):
        super(DraftEventAdminForm, self).__init__(*args, **kwargs)


class DraftEventAdmin(admin.ModelAdmin):
    """
    Model admin for DraftEvent model
    """
    date_hierarchy = 'created_at'
    list_filter = ('processed', 'source')
    ordering = ['created_at']
    search_fields = ['title',]
    inlines = [EventInline]
    actions = ["mark_processed", "mark_unprocessed"]
    list_display = ('title', 'source')
    form = DraftEventAdminForm

    def mark_processed(self, request, queryset):
        rows_updated = queryset.update(processed=True)
        self.message_user(request, "%s draft event(s) successfully marked as processed." % rows_updated)
    mark_processed.short_description = "Mark selected draft events as processed"

    def mark_unprocessed(self, request, queryset):
        rows_updated = queryset.update(processed=False)
        self.message_user(request, "%s draft event(s) successfully marked as unprocessed." % rows_updated)
    mark_unprocessed.short_description = "Mark selected draft events as unprocessed"

# admin.site.register(DraftEvent, DraftEventAdmin)


class EventRecordAdmin(admin.ModelAdmin):
    pass
# admin.site.register(EventRecord, EventRecordAdmin)


class EventAdmin(ForeignKeyAutocompleteAdmin):
    """
    Model admin for Event Model
    Note: This is similar to EventInline above
    """
    filter_horizontal = ['category']
    view_on_site = True
    prepopulated_fields = {'slug': ('title',), }
    ordering = ['-created_at']
    date_hierarchy = 'end_date'
    list_filter = (ExpiredEventListFilter, PublishedEventListFilter,)
    list_display = ('__str__', 'start_date', 'end_date')
    search_fields = ['title', 'description']
    related_search_fields = {
        'venue': ('name', 'address'),
    }
    form = EventAdminForm
    readonly_fields = ('venue_admin_url',)
    fields = ('draft', 'title', 'slug', ('venue', 'venue_admin_url',),
              'description', 'category', 'image', ('min_age', 'max_age',),
              ('cost', 'cost_detail',), ('start_date', 'end_date',),
              'recurrence_detail', 'time_detail', 'url', 'additional_info',
              'publish')

    def venue_admin_url(self, obj):
        return "<a href=http://{}{} target=\"_blank\">{}{}</a>".format(Site.objects.get_current().domain,
                                                                urlresolvers.reverse('admin:venues_venue_change',
                                                                                     args=(obj.venue.id,)),
                                                                Site.objects.get_current().domain,
                                                                urlresolvers.reverse('admin:venues_venue_change',
                                                                                     args=(obj.venue.id,)),)
    venue_admin_url.short_description = 'Edit Venue Link'
    pass

admin.site.register(Event, EventAdmin)


class CategoryAdmin(admin.ModelAdmin):

    def is_parent(obj):
        return True if not obj.parent_category else False

    prepopulated_fields = {'slug': ('name',), }
    list_display = ('name', is_parent, 'parent_category',)
admin.site.register(Category, CategoryAdmin)
