# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from apps.events.models import Event


def add_published_dates(apps, schema_editor):
    """
    If event is marked as published, call save on it
    :param apps:
    :param schema_editor:
    :return:
    """
    for event in Event.objects.all():
        if event.publish:
            event.published_at = event.created_at
            event.save()


def delete_published_dates(apps, schema_editor):
    """
    When rolling back, nothing to do
    :param apps:
    :param schema_editor:
    :return:
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150312_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='published_at',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(add_published_dates, reverse_code=delete_published_dates),
    ]
