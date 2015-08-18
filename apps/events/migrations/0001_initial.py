# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venues', '0008_auto_20150527_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200, db_index=True)),
                ('slug', models.SlugField(null=True, blank=True, help_text='The part of the title that is used in the url. Leave this blank if you want the system to generate one for you.', unique=True)),
                ('description', models.CharField(max_length=200)),
                ('font_awesome_icon_class', models.CharField(max_length=50, null=True, blank=True)),
                ('parent_category', models.ForeignKey(related_name='children', blank=True, to='events.Category', null=True)),
            ],
            options={
                'ordering': ('-parent_category__name', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200, verbose_name='Event name')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(verbose_name='Event description')),
                ('image', models.ImageField(upload_to='events_media')),
                ('min_age', models.PositiveSmallIntegerField(default=0, db_index=True)),
                ('max_age', models.PositiveSmallIntegerField(default=100, db_index=True)),
                ('cost', models.FloatField(default=0, db_index=True)),
                ('cost_detail', models.CharField(help_text='Enter if there is more than one cost value', max_length=500, blank=True)),
                ('start_date', models.DateField(db_index=True)),
                ('end_date', models.DateField(help_text='End date of the event, if applicable', null=True, db_index=True, blank=True)),
                ('recurrence_detail', models.CharField(help_text='Enter a line about when this event is till, if it is recurring', max_length=500, null=True, blank=True)),
                ('time_detail', models.CharField(help_text='Enter time for different days, in different rows', max_length=500, null=True, blank=True)),
                ('url', models.URLField(null=True, verbose_name='Event link', blank=True)),
                ('additional_info', models.TextField(null=True, blank=True)),
                ('publish', models.BooleanField(default=True)),
                ('published_at', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('view_seed', models.PositiveIntegerField(default=0)),
                ('category', models.ManyToManyField(to='events.Category', db_index=True)),
                ('suggested_by', models.ForeignKey(related_name='suggested_events', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='venues.Venue', null=True)),
            ],
            options={
                'ordering': ['-published_at', '-start_date', 'end_date'],
            },
        ),
        migrations.CreateModel(
            name='SimilarEvents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.OneToOneField(to='events.Event')),
                ('similar_events', models.ManyToManyField(related_name='+', to='events.Event')),
            ],
        ),
    ]
