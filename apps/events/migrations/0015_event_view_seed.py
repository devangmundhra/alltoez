# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.db import models, migrations

from apps.events.models import Event


def add_view_seeds(apps, schema_editor):
    """
    Add random view seed to events
    :param apps:
    :param schema_editor:
    :return:
    """
    for event in Event.objects.all():
        event.view_seed = random.randint(20, 70)
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20150610_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='view_seed',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(add_view_seeds),
    ]
