# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150119_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='publish',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
