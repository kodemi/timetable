# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Flight'
        db.create_table('vnukovo_flight', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flight', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('flight_type', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('airline', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('airport_of_departure', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('airport_of_arrival', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('flight_status', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('datetime_scheduled', self.gf('django.db.models.fields.DateTimeField')()),
            ('datetime_estimated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('datetime_actual', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('terminal', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('comment', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('checkin_desk', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
        ))
        db.send_create_signal('vnukovo', ['Flight'])

    def backwards(self, orm):
        
        # Deleting model 'Flight'
        db.delete_table('vnukovo_flight')

    models = {
        'vnukovo.flight': {
            'Meta': {'object_name': 'Flight'},
            'airline': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'airport_of_arrival': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'airport_of_departure': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'checkin_desk': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'datetime_actual': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_estimated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_scheduled': ('django.db.models.fields.DateTimeField', [], {}),
            'flight': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'flight_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'flight_type': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'terminal': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['vnukovo']
