# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields

from apps.alltoez_profile.models import UserProfile


def add_last_filter_details(apps, schema_editor):
    """
    Add user profile info for last filter detail
    :param apps:
    :param schema_editor:
    :return:
    """
    for profile in UserProfile.objects.all():
        if profile.point and profile.city:
            profile.last_filter_center = profile.point
            profile.last_filter_location_name = profile.city
            profile.last_filter_radius = 7  # 7 miles
            profile.save()


def delete_last_filter_details(apps, schema_editor):
    """
    When rolling back, nothing to do
    :param apps:
    :param schema_editor:
    :return:
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('alltoez_profile', '0003_userprofile_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_filter_center',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_filter_location_name',
            field=models.CharField(max_length=300, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_filter_radius',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(add_last_filter_details, reverse_code=delete_last_filter_details),
    ]
