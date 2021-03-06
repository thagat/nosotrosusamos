# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Tag.category'
        db.delete_column(u'cms_tag', 'category_id')

        # Adding M2M table for field categories on 'Tag'
        m2m_table_name = db.shorten_name(u'cms_tag_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm[u'cms.tag'], null=False)),
            ('category', models.ForeignKey(orm[u'cms.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tag_id', 'category_id'])


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Tag.category'
        raise RuntimeError("Cannot reverse this migration. 'Tag.category' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Tag.category'
        db.add_column(u'cms_tag', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Category']),
                      keep_default=False)

        # Removing M2M table for field categories on 'Tag'
        db.delete_table(db.shorten_name(u'cms_tag_categories'))


    models = {
        u'cms.category': {
            'Meta': {'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'cms.interview': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Interview'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dream_setup': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'interviews'", 'symmetrical': 'False', 'to': u"orm['cms.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'what_hardware': ('django.db.models.fields.TextField', [], {}),
            'what_software': ('django.db.models.fields.TextField', [], {}),
            'who_you_are': ('django.db.models.fields.TextField', [], {})
        },
        u'cms.tag': {
            'Meta': {'object_name': 'Tag'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tags'", 'symmetrical': 'False', 'to': u"orm['cms.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cms']