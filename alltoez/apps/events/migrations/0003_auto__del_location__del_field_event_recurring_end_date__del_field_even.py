# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'events_location')

        # Deleting field 'Event.recurring_end_date'
        db.delete_column(u'events_event', 'recurring_end_date')

        # Deleting field 'Event.recurring_start_date'
        db.delete_column(u'events_event', 'recurring_start_date')

        # Deleting field 'Event.recurring_frequency'
        db.delete_column(u'events_event', 'recurring_frequency')

        # Deleting field 'Event.recurring'
        db.delete_column(u'events_event', 'recurring')

        # Adding field 'Event.address'
        db.add_column(u'events_event', 'address',
                      self.gf('django.db.models.fields.TextField')(default=0),
                      keep_default=False)

        # Adding field 'Event.start_date'
        db.add_column(u'events_event', 'start_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 10, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.start_time'
        db.add_column(u'events_event', 'start_time',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2014, 10, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.end_time'
        db.add_column(u'events_event', 'end_time',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2014, 10, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.end_date'
        db.add_column(u'events_event', 'end_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.cron_recurrence_format'
        db.add_column(u'events_event', 'cron_recurrence_format',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.additional_info'
        db.add_column(u'events_event', 'additional_info',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Event.next_date'
        db.alter_column(u'events_event', 'next_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Event.location'
        db.alter_column(u'events_event', 'location', self.gf('location_field.models.PlainLocationField')(max_length=63))

    def backwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'events_location', (
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('formatted_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('address_3', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['Location'])

        # Adding field 'Event.recurring_end_date'
        db.add_column(u'events_event', 'recurring_end_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.recurring_start_date'
        db.add_column(u'events_event', 'recurring_start_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.recurring_frequency'
        db.add_column(u'events_event', 'recurring_frequency',
                      self.gf('jsonfield.fields.JSONField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.recurring'
        db.add_column(u'events_event', 'recurring',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Event.address'
        db.delete_column(u'events_event', 'address')

        # Deleting field 'Event.start_date'
        db.delete_column(u'events_event', 'start_date')

        # Deleting field 'Event.start_time'
        db.delete_column(u'events_event', 'start_time')

        # Deleting field 'Event.end_time'
        db.delete_column(u'events_event', 'end_time')

        # Deleting field 'Event.end_date'
        db.delete_column(u'events_event', 'end_date')

        # Deleting field 'Event.cron_recurrence_format'
        db.delete_column(u'events_event', 'cron_recurrence_format')

        # Deleting field 'Event.additional_info'
        db.delete_column(u'events_event', 'additional_info')


        # Changing field 'Event.next_date'
        db.alter_column(u'events_event', 'next_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Event.location'
        db.alter_column(u'events_event', 'location', self.gf('jsonfield.fields.JSONField')())

    models = {
        u'events.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'events.draftevent': {
            'Meta': {'object_name': 'DraftEvent'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'raw': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'events.event': {
            'Meta': {'ordering': "['next_date', 'start_time']", 'object_name': 'Event'},
            'additional_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.Category']", 'db_index': 'True', 'symmetrical': 'False'}),
            'cost': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cron_recurrence_format': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.DraftEvent']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('jsonfield.fields.JSONField', [], {'default': '\'{"url":"","source_name":"","source_url":""}\''}),
            'location': ('location_field.models.PlainLocationField', [], {'max_length': '63'}),
            'max_age': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '100'}),
            'min_age': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'next_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'events.eventrecord': {
            'Meta': {'ordering': "['date']", 'unique_together': "(('event', 'date'),)", 'object_name': 'EventRecord'},
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['events']