# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_event_published_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-published_at', '-start_date', 'end_date']},
        ),
        migrations.AlterField(
            model_name='event',
            name='cost',
            field=models.FloatField(default=0, db_index=True),
            preserve_default=True,
        ),
    ]
