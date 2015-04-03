# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('alltoez_profile', '0002_auto_20150207_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
    ]
