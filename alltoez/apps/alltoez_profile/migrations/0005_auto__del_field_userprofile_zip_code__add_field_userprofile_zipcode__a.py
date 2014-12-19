# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserProfile.zip_code'
        db.delete_column(u'alltoez_profile_userprofile', 'zip_code')

        # Adding field 'UserProfile.zipcode'
        db.add_column(u'alltoez_profile_userprofile', 'zipcode',
                      self.gf('django.db.models.fields.CharField')(db_index=True, default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.longitude'
        db.add_column(u'alltoez_profile_userprofile', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=15, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.latitude'
        db.add_column(u'alltoez_profile_userprofile', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(db_index=True, null=True, max_digits=15, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.address'
        db.add_column(u'alltoez_profile_userprofile', 'address',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.address_line_2'
        db.add_column(u'alltoez_profile_userprofile', 'address_line_2',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.address_line_3'
        db.add_column(u'alltoez_profile_userprofile', 'address_line_3',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.city'
        db.add_column(u'alltoez_profile_userprofile', 'city',
                      self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.state'
        db.add_column(u'alltoez_profile_userprofile', 'state',
                      self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.country'
        db.add_column(u'alltoez_profile_userprofile', 'country',
                      self.gf('apps.alltoez.utils.fields.CountryField')(default='US', max_length=2, null=True, db_index=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'UserProfile.zip_code'
        db.add_column(u'alltoez_profile_userprofile', 'zip_code',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=10),
                      keep_default=False)

        # Deleting field 'UserProfile.zipcode'
        db.delete_column(u'alltoez_profile_userprofile', 'zipcode')

        # Deleting field 'UserProfile.longitude'
        db.delete_column(u'alltoez_profile_userprofile', 'longitude')

        # Deleting field 'UserProfile.latitude'
        db.delete_column(u'alltoez_profile_userprofile', 'latitude')

        # Deleting field 'UserProfile.address'
        db.delete_column(u'alltoez_profile_userprofile', 'address')

        # Deleting field 'UserProfile.address_line_2'
        db.delete_column(u'alltoez_profile_userprofile', 'address_line_2')

        # Deleting field 'UserProfile.address_line_3'
        db.delete_column(u'alltoez_profile_userprofile', 'address_line_3')

        # Deleting field 'UserProfile.city'
        db.delete_column(u'alltoez_profile_userprofile', 'city')

        # Deleting field 'UserProfile.state'
        db.delete_column(u'alltoez_profile_userprofile', 'state')

        # Deleting field 'UserProfile.country'
        db.delete_column(u'alltoez_profile_userprofile', 'country')


    models = {
        u'alltoez_profile.child': {
            'Meta': {'object_name': 'Child'},
            'age': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': "''", 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': u"orm['auth.User']"})
        },
        u'alltoez_profile.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'address_line_2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'address_line_3': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'country': ('apps.alltoez.utils.fields.CountryField', [], {'default': "'US'", 'max_length': '2', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '15', 'decimal_places': '8', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '15', 'decimal_places': '8', 'blank': 'True'}),
            'profile_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['alltoez_profile']