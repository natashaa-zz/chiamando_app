# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SOTSadmin'
        db.create_table(u'sots_sotsadmin', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True, db_index=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'sots', ['SOTSadmin'])

        # Adding model 'SOTSCallRecord'
        db.create_table(u'sots_sotscallrecord', (
            ('ssrecid', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_index=True)),
            ('familyid', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('middlename', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('mobile1', self.gf('django.db.models.fields.IntegerField')()),
            ('mobile2', self.gf('django.db.models.fields.IntegerField')()),
            ('landline', self.gf('django.db.models.fields.IntegerField')()),
            ('emergency_contact1_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('emergency_contact1', self.gf('django.db.models.fields.IntegerField')()),
            ('emergency_contact2_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('emergency_contact2', self.gf('django.db.models.fields.IntegerField')()),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('round1_mobile1_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round1_mobile2_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round1_landline_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round1_sotsuser', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='round1_sotsuser', null=True, on_delete=models.SET_NULL, to=orm['sots.SOTSadmin'])),
            ('round1_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('round2_mobile1_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round2_mobile2_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round2_landline_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round2_sotsuser', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='round2_sotsuser', null=True, on_delete=models.SET_NULL, to=orm['sots.SOTSadmin'])),
            ('round2_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('round3_mobile1_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round3_mobile2_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round3_landline_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round3_emergency_contact1_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round3_emergency_contact2_status', self.gf('django.db.models.fields.CharField')(default='', max_length=4, db_index=True, blank=True)),
            ('round3_sotsuser', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='round3_sotsuser', null=True, on_delete=models.SET_NULL, to=orm['sots.SOTSadmin'])),
            ('round3_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('contacted_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'sots', ['SOTSCallRecord'])


    def backwards(self, orm):
        # Deleting model 'SOTSadmin'
        db.delete_table(u'sots_sotsadmin')

        # Deleting model 'SOTSCallRecord'
        db.delete_table(u'sots_sotscallrecord')


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
            'contacted_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'emergency_contact1': ('django.db.models.fields.IntegerField', [], {}),
            'emergency_contact1_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'emergency_contact2': ('django.db.models.fields.IntegerField', [], {}),
            'emergency_contact2_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'familyid': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'landline': ('django.db.models.fields.IntegerField', [], {}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'middlename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mobile1': ('django.db.models.fields.IntegerField', [], {}),
            'mobile2': ('django.db.models.fields.IntegerField', [], {}),
            'round1_landline_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round1_mobile1_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round1_mobile2_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round1_sotsuser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'round1_sotsuser'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['sots.SOTSadmin']"}),
            'round1_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'round2_landline_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round2_mobile1_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round2_mobile2_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round2_sotsuser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'round2_sotsuser'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['sots.SOTSadmin']"}),
            'round2_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'round3_emergency_contact1_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round3_emergency_contact2_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round3_landline_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round3_mobile1_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round3_mobile2_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'db_index': 'True', 'blank': 'True'}),
            'round3_sotsuser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'round3_sotsuser'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['sots.SOTSadmin']"}),
            'round3_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'ssrecid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['sots']