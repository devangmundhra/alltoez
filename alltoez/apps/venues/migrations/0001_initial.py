# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Venue'
        db.create_table(u'venues_venue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=15, decimal_places=8, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=15, decimal_places=8, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('address_line_2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('address_line_3', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, blank=True)),
            ('country', self.gf('apps.alltoez.utils.fields.CountryField')(default='US', max_length=2, null=True, db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Unspecified', max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('phone_number', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=63, null=True, blank=True)),
        ))
        db.send_create_signal(u'venues', ['Venue'])


    def backwards(self, orm):
        # Deleting model 'Venue'
        db.delete_table(u'venues_venue')


    models = {
        u'venues.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'address_line_2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'address_line_3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'country': ('apps.alltoez.utils.fields.CountryField', [], {'default': "'US'", 'max_length': '2', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '15', 'decimal_places': '8', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '15', 'decimal_places': '8', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Unspecified'", 'max_length': '200'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['venues']