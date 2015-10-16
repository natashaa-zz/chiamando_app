# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SOTSCallRecord.emergency_contact1'
        db.alter_column(u'sots_sotscallrecord', 'emergency_contact1', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'SOTSCallRecord.emergency_contact2'
        db.alter_column(u'sots_sotscallrecord', 'emergency_contact2', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'SOTSCallRecord.landline'
        db.alter_column(u'sots_sotscallrecord', 'landline', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Changing field 'SOTSCallRecord.mobile1'
        db.alter_column(u'sots_sotscallrecord', 'mobile1', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Changing field 'SOTSCallRecord.mobile2'
        db.alter_column(u'sots_sotscallrecord', 'mobile2', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

    def backwards(self, orm):

        # Changing field 'SOTSCallRecord.emergency_contact1'
        db.alter_column(u'sots_sotscallrecord', 'emergency_contact1', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'SOTSCallRecord.emergency_contact2'
        db.alter_column(u'sots_sotscallrecord', 'emergency_contact2', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'SOTSCallRecord.landline'
        db.alter_column(u'sots_sotscallrecord', 'landline', self.gf('django.db.models.fields.BigIntegerField')(null=True))

        # Changing field 'SOTSCallRecord.mobile1'
        db.alter_column(u'sots_sotscallrecord', 'mobile1', self.gf('django.db.models.fields.BigIntegerField')(default=0))

        # Changing field 'SOTSCallRecord.mobile2'
        db.alter_column(u'sots_sotscallrecord', 'mobile2', self.gf('django.db.models.fields.BigIntegerField')(null=True))

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
            'current_round': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'emergency_contact1': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'emergency_contact1_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'emergency_contact2': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'emergency_contact2_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'familyid': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'landline': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'middlename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mobile1': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'mobile2': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'overall_status': ('django.db.models.fields.CharField', [], {'default': "'NI'", 'max_length': '4', 'db_index': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'round1_landline_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round1_mobile1_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round1_mobile2_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round1_sotsuser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'round1_sotsuser'", 'null': 'True', 'to': u"orm['sots.SOTSadmin']"}),
            'round1_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'round2_landline_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round2_mobile1_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round2_mobile2_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round2_sotsuser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'round2_sotsuser'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['sots.SOTSadmin']"}),
            'round2_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'round3_emergency_contact1_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round3_emergency_contact2_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round3_landline_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round3_mobile1_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round3_mobile2_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'round3_sotsuser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'round3_sotsuser'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['sots.SOTSadmin']"}),
            'round3_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ssrecid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['sots']