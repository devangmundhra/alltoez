__author__ = 'devangmundhra'

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.user_actions.models import Bookmark, Done, Review


class UserActionAbstractSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        abstract = True


class DoneSerializer(UserActionAbstractSerializer):
    resource_uri = serializers.SerializerMethodField(read_only=True)

    class Meta(UserActionAbstractSerializer.Meta):
        model = Done

    def get_resource_uri(self, obj):
        request = self.context.get('request')
        return reverse('api:done-detail', args=[obj, 'json'], request=request)


class BookmarkSerializer(UserActionAbstractSerializer):
    resource_uri = serializers.SerializerMethodField(read_only=True)

    class Meta(UserActionAbstractSerializer.Meta):
        model = Bookmark

    def get_resource_uri(self, obj):
        request = self.context.get('request')
        return reverse('api:bookmark-detail', args=[obj, 'json'], request=request)


class ReviewSerializer(UserActionAbstractSerializer):
    comment = serializers.CharField(style={'base_template': 'textarea.html'}, required=False, allow_blank=True)

    class Meta(UserActionAbstractSerializer.Meta):
        model = Review
