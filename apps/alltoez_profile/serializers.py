__author__ = 'devangmundhra'
from django.contrib.auth.models import User

from rest_framework import serializers

from apps.alltoez_profile.models import UserProfile, Child


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child


class AlltoezProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile


class UserInternalSerializer(serializers.HyperlinkedModelSerializer):
    children = ChildSerializer(many=True, required=False)
    profile = AlltoezProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'pk', 'username', 'first_name', 'last_name', 'email', 'children', 'profile')