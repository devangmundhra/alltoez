# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0011_auto_20150419_0756'),
        ('user_actions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('rating', models.PositiveSmallIntegerField(default=0, verbose_name=b'rating', choices=[(0, b'No Rating'), (1, b'One Star'), (2, b'Two Star'), (3, b'Three Star'), (4, b'Four Star'), (5, b'Five Star')])),
                ('comment', models.TextField()),
                ('event', models.ForeignKey(to='events.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('user', 'event')]),
        ),
    ]
