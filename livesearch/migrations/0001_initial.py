
from south.db import db
from django.db import models
from muaccounts.models import *
from livesearch.models import *

class Migration:

    depends_on = (
        ("muaccounts", "0002_nullable_owner"),
    )
        
    def forwards(self, orm):
        
        # Adding model 'AdvancedSearch'
        db.create_table('livesearch_advancedsearch', (
            ('id', orm['livesearch.AdvancedSearch:id']),
            ('count', orm['livesearch.AdvancedSearch:count']),
            ('market', orm['livesearch.AdvancedSearch:market']),
            ('user', orm['livesearch.AdvancedSearch:user']),
        ))
        db.send_create_signal('livesearch', ['AdvancedSearch'])
        
        # Adding model 'SearchApi'
        db.create_table('livesearch_searchapi', (
            ('id', orm['livesearch.SearchApi:id']),
            ('name', orm['livesearch.SearchApi:name']),
            ('slug', orm['livesearch.SearchApi:slug']),
            ('search_model', orm['livesearch.SearchApi:search_model']),
        ))
        db.send_create_signal('livesearch', ['SearchApi'])
        
        # Adding ManyToManyField 'SearchApi.muaccount'
        db.create_table('livesearch_searchapi_muaccount', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('searchapi', models.ForeignKey(orm.SearchApi, null=False)),
            ('muaccount', models.ForeignKey(orm['muaccounts.MUAccount'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'AdvancedSearch'
        db.delete_table('livesearch_advancedsearch')
        
        # Deleting model 'SearchApi'
        db.delete_table('livesearch_searchapi')
        
        # Dropping ManyToManyField 'SearchApi.muaccount'
        db.delete_table('livesearch_searchapi_muaccount')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'livesearch.advancedsearch': {
            'count': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'livesearch.searchapi': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muaccount': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['muaccounts.MUAccount']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'search_model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'})
        },
        'muaccounts.muaccount': {
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '256', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'logo': ('RemovableImageField', [], {'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'max_length': '256', 'unique': 'True', 'null': 'True'}),
            'theme': ('PickledObjectField', [], {'default': '( lambda :DEFAULT_THEME_DICT)'})
        }
    }
    
    complete_apps = ['livesearch']
