# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0013_remove_event_image_info'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventrecord',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='eventrecord',
            name='event',
        ),
        migrations.RemoveField(
            model_name='event',
            name='draft',
        ),
        migrations.AddField(
            model_name='event',
            name='suggested_by',
            field=models.ForeignKey(related_name='suggested_events', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.DeleteModel(
            name='DraftEvent',
        ),
        migrations.DeleteModel(
            name='EventRecord',
        ),
    ]
