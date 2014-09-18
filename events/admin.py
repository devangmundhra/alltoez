from django.contrib import admin

from events.models import DraftEvent, Event, EventRecord

class DraftEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(DraftEvent, DraftEventAdmin)

class EventAdmin(admin.ModelAdmin):
    pass
admin.site.register(Event, EventAdmin)

class EventRecordAdmin(admin.ModelAdmin):
    pass
admin.site.register(EventRecord, EventRecordAdmin)