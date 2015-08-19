# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


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
    ]
