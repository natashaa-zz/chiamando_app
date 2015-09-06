# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SOTSCallRecord.round3_timestamp'
        db.alter_column(u'sots_sotscallrecord', 'round3_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'SOTSCallRecord.round1_timestamp'
        db.alter_column(u'sots_sotscallrecord', 'round1_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'SOTSCallRecord.emergency_contact1'
        db.alter_column(u'sots_sotscallrecord', 'emergency_contact1', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'SOTSCallRecord.emergency_contact2'
        db.alter_column(u'sots_sotscallrecord', 'emergency_contact2', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'SOTSCallRecord.landline'
        db.alter_column(u'sots_sotscallrecord', 'landline', self.gf('django.db.models.fields.BigIntegerField')(null=True))

        # Changing field 'SOTSCallRecord.contacted_number'
        db.alter_column(u'sots_sotscallrecord', 'contacted_number', self.gf('django.db.models.fields.BigIntegerField')(null=True))

        # Changing field 'SOTSCallRecord.round2_timestamp'
        db.alter_column(u'sots_sotscallrecord', 'round2_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'SOTSCallRecord.mobile1'
        db.alter_column(u'sots_sotscallrecord', 'mobile1', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'SOTSCallRecord.mobile2'
        db.alter_column(u'sots_sotscallrecord', 'mobile2', self.gf('django.db.models.fields.BigIntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'SOTSCallRecord.round3_timestamp'
        db.alter_column(u'sots_sotscallrecord', 'round3_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 8, 16, 0, 0)))

        # Changing field 'SOTSCallRecord.round1_timestamp'
        db.alter_column(u'sots_sotscallrecord', 'round1_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 8, 16, 0, 0)))

        # Changing field 'SOTSCallRecord.emergency_contact1'
        db.alter_column(u'sots_sotscallrecord', 'emergency_contact1', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'SOTSCallRecord.emergency_contact2'
        db.alter_column(u'sots_sotscallrecord', 'emergency_contact2', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'SOTSCallRecord.landline'
        db.alter_column(u'sots_sotscallrecord', 'landline', self.gf('django.db.models.fields.IntegerField')(default=datetime.datetime(2015, 8, 16, 0, 0)))

        # Changing field 'SOTSCallRecord.contacted_number'
        db.alter_column(u'sots_sotscallrecord', 'contacted_number', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'SOTSCallRecord.round2_timestamp'
        db.alter_column(u'sots_sotscallrecord', 'round2_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 8, 16, 0, 0)))

        # Changing field 'SOTSCallRecord.mobile1'
        db.alter_column(u'sots_sotscallrecord', 'mobile1', self.gf('django.db.models.fields.IntegerField')())

        # User chose to not deal with backwards NULL issues for 'SOTSCallRecord.mobile2'
        raise RuntimeError("Cannot reverse this migration. 'SOTSCallRecord.mobile2' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'SOTSCallRecord.mobile2'
        db.alter_column(u'sots_sotscallrecord', 'mobile2', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'sots.sotsadmin': {
            'Meta': {'object_name': 'SOTSadmin'},
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        u'sots.sotscallrecord': {
            'Meta': {'object_name': 'SOTSCallRecord'},
            'contacted_number': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'emergency_contact1': ('django.db.models.fields.BigIntegerField', [], {}),
            'emergency_contact1_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'emergency_contact2': ('django.db.models.fields.BigIntegerField', [], {}),
            'emergency_contact2_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'familyid': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'landline': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'middlename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mobile1': ('django.db.models.fields.BigIntegerField', [], {}),
            'mobile2': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'overall_status': ('django.db.models.fields.CharField', [], {'default': "'NI'", 'max_length': '4', 'db_index': 'True'}),
            'round1_landline_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round1_mobile1_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round1_mobile2_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round1_sotsuser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'round1_sotsuser'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['sots.SOTSadmin']"}),
            'round1_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'round2_landline_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round2_mobile1_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round2_mobile2_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round2_sotsuser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'round2_sotsuser'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['sots.SOTSadmin']"}),
            'round2_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'round3_emergency_contact1_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round3_emergency_contact2_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round3_landline_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round3_mobile1_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round3_mobile2_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round3_sotsuser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'round3_sotsuser'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['sots.SOTSadmin']"}),
            'round3_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ssrecid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['sots']