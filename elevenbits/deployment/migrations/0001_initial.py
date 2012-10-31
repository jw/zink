# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Deployment'
        db.create_table('deployment_deployment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(unique=True)),
            ('deployer', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('deployment', ['Deployment'])


    def backwards(self, orm):
        # Deleting model 'Deployment'
        db.delete_table('deployment_deployment')


    models = {
        'deployment.deployment': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Deployment'},
            'deployer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'unique': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['deployment']