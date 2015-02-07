# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0004_auto_20150119_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='raw_address',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='venue',
            name='state',
            field=models.CharField(default='CA', max_length=150, null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
    ]
