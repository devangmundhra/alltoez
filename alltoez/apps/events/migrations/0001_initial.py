# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'events_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Category'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'events', ['Category'])

        # Adding model 'DraftEvent'
        db.create_table(u'events_draftevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('raw', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=200, unique=True, null=True, blank=True)),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'events', ['DraftEvent'])

        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('draft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.DraftEvent'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('location', self.gf('location_field.models.PlainLocationField')(max_length=63)),
            ('image', self.gf('jsonfield.fields.JSONField')(default='{"url":"","source_name":"","source_url":""}')),
            ('min_age', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('max_age', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=100)),
            ('cost', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('next_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('cron_recurrence_format', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, unique=True, null=True, blank=True)),
            ('additional_info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding M2M table for field category on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('category', models.ForeignKey(orm[u'events.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'category_id'])

        # Adding model 'EventRecord'
        db.create_table(u'events_eventrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal(u'events', ['EventRecord'])

        # Adding unique constraint on 'EventRecord', fields ['event', 'date']
        db.create_unique(u'events_eventrecord', ['event_id', 'date'])


    def backwards(self, orm):
        # Removing unique constraint on 'EventRecord', fields ['event', 'date']
        db.delete_unique(u'events_eventrecord', ['event_id', 'date'])

        # Deleting model 'Category'
        db.delete_table(u'events_category')

        # Deleting model 'DraftEvent'
        db.delete_table(u'events_draftevent')

        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Removing M2M table for field category on 'Event'
        db.delete_table(db.shorten_name(u'events_event_category'))

        # Deleting model 'EventRecord'
        db.delete_table(u'events_eventrecord')


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