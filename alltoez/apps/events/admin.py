from datetime import datetime

from django.contrib import admin
from django import forms

from croniter import croniter
from splitjson.widgets import SplitJSONWidget

from apps.events.models import DraftEvent, Event, EventRecord, Category


class EventAdminForm(forms.ModelForm):
    """
    Custom form for event admin form
    """
    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = SplitJSONWidget()

    def clean_cron_recurrence_format(self):
        cur_cron_format = self.cleaned_data['cron_recurrence_format']
        if cur_cron_format is not None:
            try:
                base = datetime.now()
                cron = croniter(cur_cron_format, base)
                cron.get_current()
            except:
                raise forms.ValidationError("Cron format invalid", code="invalid")

        return cur_cron_format

    def clean(self):
        cur_cron_format = self.cleaned_data['cron_recurrence_format']
        if cur_cron_format is not None:
            cur_start_date = self.cleaned_data['start_date']
            cur_start_time = self.cleaned_data['start_time']
            cron = croniter(cur_cron_format, datetime.combine(cur_start_date, cur_start_time))
            next_date = cron.get_next(datetime)
            if next_date.date() == cur_start_date:
                raise forms.ValidationError("Cron format is probably incorrect. "
                "Next occurance of event seems to be on the same day", code="incorrect")

        return self.cleaned_data

class EventInline(admin.StackedInline):
    """
    Inline model form to edit event information
    Note: This is similar to EventAdmin below
    """
    model = Event
    exclude = ('slug',)
    max_num = 1
    form = EventAdminForm


class DraftEventAdminForm(forms.ModelForm):
    """
    Custom form for DraftEvent admin form
    """
    def __init__(self, *args, **kwargs):
        super(DraftEventAdminForm, self).__init__(*args, **kwargs)
        self.fields['raw'].widget = SplitJSONWidget()

class DraftEventAdmin(admin.ModelAdmin):
    """
    Model admin for DraftEvent model
    """
    date_hierarchy = 'created_at'
    list_filter = ('processed', 'source')
    ordering = ['created_at']
    search_fields = ['title',]
    inlines = [EventInline]
    actions = ["mark_processed"]
    list_display = ('title', 'source')
    form = DraftEventAdminForm

    def mark_processed(self, request, queryset):
        rows_updated = queryset.update(processed=True)
        self.message_user(request, "%s draft event(s) successfully marked as processed." % rows_updated)
    mark_processed.short_description = "Mark selected draft events as processed"

admin.site.register(DraftEvent, DraftEventAdmin)

class EventRecordAdmin(admin.ModelAdmin):
    pass
admin.site.register(EventRecord, EventRecordAdmin)

class EventAdmin(admin.ModelAdmin):
    """
    Model admin for Event Model
    Note: This is similar to EventInline above
    """
    prepopulated_fields = {'slug': ('title',), }
    exclude = ('slug',)
    search_fields = ['title', 'description']
    form = EventAdminForm

admin.site.register(Event, EventAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
admin.site.register(Category, CategoryAdmin)
