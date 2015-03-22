# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20141230_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time_detail',
            field=models.CharField(help_text=b'Enter time for different days, in different rows', max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
