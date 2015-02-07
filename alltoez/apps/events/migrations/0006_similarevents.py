# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_publish'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimilarEvents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(to='events.Event', unique=True)),
                ('similar_events', models.ManyToManyField(related_name='+', to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
