from django.contrib import admin

from apps.user_actions.models import View, Done, Bookmark, Share

admin.site.register(View)
admin.site.register(Done)
admin.site.register(Bookmark)
admin.site.register(Share)