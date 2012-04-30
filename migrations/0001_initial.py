# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('wiki_page', (
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=30, primary_key=True, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('current_revision', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wiki.PageRevision'])),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('next_revision_num', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
        ))
        db.send_create_signal('wiki', ['Page'])

        # Adding model 'PageRevision'
        db.create_table('wiki_pagerevision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Page'])),
            ('num', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pagerevision_set_created', to=orm['auth.User'])),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('previous_revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.PageRevision'], null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=100000, blank=True)),
            ('reverted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('revert_reason', self.gf('django.db.models.fields.TextField')(max_length=50, blank=True)),
            ('revert_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pagerevision_set_reverted', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('wiki', ['PageRevision'])

        # Adding model 'PageUser'
        db.create_table('wiki_pageuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='page_set', to=orm['auth.User'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_set', to=orm['wiki.Page'])),
            ('first_view', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('last_view', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('last_view_revision', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('wiki', ['PageUser'])


    def backwards(self, orm):
        
        # Deleting model 'Page'
        db.delete_table('wiki_page')

        # Deleting model 'PageRevision'
        db.delete_table('wiki_pagerevision')

        # Deleting model 'PageUser'
        db.delete_table('wiki_pageuser')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'wiki.page': {
            'Meta': {'object_name': 'Page'},
            'current_revision': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['wiki.PageRevision']"}),
            'next_revision_num': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '30', 'primary_key': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'wiki.pagerevision': {
            'Meta': {'object_name': 'PageRevision'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pagerevision_set_created'", 'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '100000', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Page']"}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.PageRevision']", 'null': 'True', 'blank': 'True'}),
            'revert_reason': ('django.db.models.fields.TextField', [], {'max_length': '50', 'blank': 'True'}),
            'revert_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pagerevision_set_reverted'", 'null': 'True', 'to': "orm['auth.User']"}),
            'reverted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'wiki.pageuser': {
            'Meta': {'object_name': 'PageUser'},
            'first_view': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_view': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'last_view_revision': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_set'", 'to': "orm['wiki.Page']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'page_set'", 'to': "orm['auth.User']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        }
    }

    complete_apps = ['wiki']
