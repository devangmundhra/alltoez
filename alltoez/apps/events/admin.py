from django.contrib import admin
from apps.events.models import DraftEvent, Event, EventRecord, Category

class DraftEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(DraftEvent, DraftEventAdmin)

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
admin.site.register(Event, EventAdmin)

class EventRecordAdmin(admin.ModelAdmin):
    pass
admin.site.register(EventRecord, EventRecordAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
admin.site.register(Category, CategoryAdmin)
