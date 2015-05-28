# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20150508_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='image_info',
        ),
    ]
