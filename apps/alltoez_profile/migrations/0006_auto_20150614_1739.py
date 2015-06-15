# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('alltoez_profile', '0005_userprofile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_filter_center',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_filter_location_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_filter_radius',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_known_location_bounds',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_map_zoom',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
    ]
