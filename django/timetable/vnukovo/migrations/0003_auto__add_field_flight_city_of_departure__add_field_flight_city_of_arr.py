# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Flight.city_of_departure'
        db.add_column('vnukovo_flight', 'city_of_departure', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        # Adding field 'Flight.city_of_arrival'
        db.add_column('vnukovo_flight', 'city_of_arrival', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

    def backwards(self, orm):
        
        # Deleting field 'Flight.city_of_departure'
        db.delete_column('vnukovo_flight', 'city_of_departure')

        # Deleting field 'Flight.city_of_arrival'
        db.delete_column('vnukovo_flight', 'city_of_arrival')

    models = {
        'vnukovo.flight': {
            'Meta': {'object_name': 'Flight'},
            'airline': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'airport': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'airport_of_arrival': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'airport_of_departure': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'checkin_desk': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'city_of_arrival': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city_of_departure': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
