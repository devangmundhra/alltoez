from django.contrib import admin
from django import forms

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from apps.events.models import DraftEvent, Event, EventRecord, Category


class EventAdminForm(forms.ModelForm):
    """
    Custom form for event admin form
    """
    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = SummernoteWidget()
        self.fields['time_detail'].widget = SummernoteWidget()
        self.fields['additional_info'].widget = SummernoteWidget()


class EventInline(admin.StackedInline):
    """
    Inline model form to edit event information
    Note: This is similar to EventAdmin below
    """
    model = Event
    exclude = ('slug',)
    max_num = 1
    extra = 1
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
    ordering = ['-created_at']
    search_fields = ['title', 'description']
    form = EventAdminForm
    pass

admin.site.register(Event, EventAdmin)


class CategoryAdmin(admin.ModelAdmin):

    def is_parent(obj):
        return True if not obj.parent_category else False

    prepopulated_fields = {'slug': ('name',), }
    list_display = ('name', is_parent, 'parent_category',)
admin.site.register(Category, CategoryAdmin)
