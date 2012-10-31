# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Static'
        db.create_table('static_static', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('static', ['Static'])


    def backwards(self, orm):
        # Deleting model 'Static'
        db.delete_table('static_static')


    models = {
        'static.static': {
            'Meta': {'object_name': 'Static'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['static']