# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('slug', models.SlugField(help_text=b'The part of the title that is used in the url. Leave this blank if you want the system to generate one for you.', null=True, blank=True)),
                ('description', models.CharField(max_length=200)),
                ('font_awesome_icon_class', models.CharField(max_length=50, null=True, blank=True)),
                ('parent_category', models.ForeignKey(related_name='children', blank=True, to='events.Category', null=True)),
            ],
            options={
                'ordering': ('-parent_category__name', 'name'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DraftEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('raw', models.TextField(unique=True)),
                ('source', models.CharField(max_length=200)),
                ('source_url', models.URLField(unique=True, null=True, blank=True)),
                ('processed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('image', jsonfield.fields.JSONField(default=b'{"url":"","source_name":"","source_url":""}')),
                ('min_age', models.PositiveSmallIntegerField(default=0, db_index=True)),
                ('max_age', models.PositiveSmallIntegerField(default=100, db_index=True)),
                ('cost', models.PositiveSmallIntegerField(default=0, db_index=True)),
                ('cost_detail', models.CharField(help_text=b'Enter if there is more than one cost value', max_length=500, blank=True)),
                ('start_date', models.DateField(db_index=True)),
                ('end_date', models.DateField(help_text=b'End date of the event, if applicable', null=True, db_index=True, blank=True)),
                ('recurrence_detail', models.CharField(help_text=b'Enter a line about when this event is till, if it is recurring', max_length=500, null=True, blank=True)),
                ('time_detail', models.CharField(help_text=b'Enter time for different days, in different rows', max_length=500)),
                ('url', models.URLField(null=True, blank=True)),
                ('additional_info', models.TextField(null=True, blank=True)),
                ('category', models.ManyToManyField(to='events.Category', db_index=True)),
                ('draft', models.ForeignKey(blank=True, to='events.DraftEvent', null=True)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='venues.Venue', null=True)),
            ],
            options={
                'ordering': ['-created_at', '-start_date', 'end_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(db_index=True)),
                ('event', models.ForeignKey(to='events.Event')),
            ],
            options={
                'ordering': ['date'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='eventrecord',
            unique_together=set([('event', 'date')]),
        ),
    ]
