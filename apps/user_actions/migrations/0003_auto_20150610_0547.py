# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_actions', '0002_auto_20150424_0541'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewIP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.GenericIPAddressField(db_index=True)),
                ('count', models.IntegerField(default=0)),
                ('event', models.ForeignKey(to='events.Event')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='viewip',
            unique_together=set([('ip_address', 'event')]),
        ),
    ]
