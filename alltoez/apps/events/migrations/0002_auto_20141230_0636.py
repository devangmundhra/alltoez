# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(verbose_name=b'Event description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=200, verbose_name=b'Event name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.URLField(null=True, verbose_name=b'Event link', blank=True),
            preserve_default=True,
        ),
    ]
