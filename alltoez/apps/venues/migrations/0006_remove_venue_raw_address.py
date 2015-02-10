# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0005_auto_20150207_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='raw_address',
        ),
    ]
