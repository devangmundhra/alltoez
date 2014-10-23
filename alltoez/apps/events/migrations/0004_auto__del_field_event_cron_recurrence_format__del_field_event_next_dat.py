# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Event.cron_recurrence_format'
        db.delete_column(u'events_event', 'cron_recurrence_format')

        # Deleting field 'Event.next_date'
        db.delete_column(u'events_event', 'next_date')

        # Deleting field 'Event.start_time'
        db.delete_column(u'events_event', 'start_time')

        # Deleting field 'Event.end_time'
        db.delete_column(u'events_event', 'end_time')

        # Adding field 'Event.neighborhood'
        db.add_column(u'events_event', 'neighborhood',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.cost_detail'
        db.add_column(u'events_event', 'cost_detail',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=500),
                      keep_default=False)

        # Adding field 'Event.recurrence_detail'
        db.add_column(u'events_event', 'recurrence_detail',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.time_detail'
        db.add_column(u'events_event', 'time_detail',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=500),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Event.cron_recurrence_format'
        db.add_column(u'events_event', 'cron_recurrence_format',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.next_date'
        db.add_column(u'events_event', 'next_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.start_time'
        db.add_column(u'events_event', 'start_time',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2014, 10, 22, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.end_time'
        db.add_column(u'events_event', 'end_time',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2014, 10, 22, 0, 0)),
                      keep_default=False)

        # Deleting field 'Event.neighborhood'
        db.delete_column(u'events_event', 'neighborhood')

        # Deleting field 'Event.cost_detail'
        db.delete_column(u'events_event', 'cost_detail')

        # Deleting field 'Event.recurrence_detail'
        db.delete_column(u'events_event', 'recurrence_detail')

        # Deleting field 'Event.time_detail'
        db.delete_column(u'events_event', 'time_detail')


    models = {
        u'events.category': {
            'Meta': {'ordering': "('-parent_category__name', 'name')", 'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'font_awesome_icon_class': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['events.Category']"}),
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
            'Meta': {'ordering': "['-start_date', 'end_date']", 'object_name': 'Event'},
            'additional_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.Category']", 'db_index': 'True', 'symmetrical': 'False'}),
            'cost': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'cost_detail': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.DraftEvent']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('jsonfield.fields.JSONField', [], {'default': '\'{"url":"","source_name":"","source_url":""}\''}),
            'location': ('location_field.models.plain.PlainLocationField', [], {'max_length': '63'}),
            'max_age': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '100'}),
            'min_age': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'recurrence_detail': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'time_detail': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'events.eventrecord': {
            'Meta': {'ordering': "['date']", 'unique_together': "(('event', 'date'),)", 'object_name': 'EventRecord'},
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['events']