from django.contrib import admin

from apps.user_actions.models import ViewIP, Done, Bookmark, Share, Review


class UserActionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'event')

admin.site.register(ViewIP)
admin.site.register(Done, UserActionAdmin)
admin.site.register(Bookmark, UserActionAdmin)
admin.site.register(Share, UserActionAdmin)
admin.site.register(Review, UserActionAdmin)