# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150419_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='similarevents',
            name='event',
            field=models.OneToOneField(to='events.Event'),
        ),
    ]
