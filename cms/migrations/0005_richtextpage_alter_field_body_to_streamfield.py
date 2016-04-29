# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 13:52
from __future__ import unicode_literals

import cms.models.streamfield
from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_withintroduction_alter_field_to_streamfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='richtextpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'h5', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), (b'pullquote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.TextBlock('quote title')), (b'attribution', wagtail.wagtailcore.blocks.CharBlock())])), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.RichTextBlock()), (b'alignment', cms.models.streamfield.ImageFormatChoiceBlock())], icon='image', label='Aligned image')), (b'link', wagtail.wagtailcore.blocks.StructBlock([(b'page', wagtail.wagtailcore.blocks.PageChooserBlock(icon='wagtail', required=False)), (b'url', wagtail.wagtailcore.blocks.URLBlock(icon='link', required=False)), (b'document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False)), (b'email', cms.models.streamfield.EmailBlock(icon='mail', required=False)), (b'label', wagtail.wagtailcore.blocks.CharBlock(max_length=32))])), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), (b'html', wagtail.wagtailcore.blocks.StructBlock([(b'html', wagtail.wagtailcore.blocks.RawHTMLBlock()), (b'alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], label='Raw HTML')), (b'map_html', wagtail.wagtailcore.blocks.StructBlock([(b'html', wagtail.wagtailcore.blocks.RawHTMLBlock()), (b'alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], label='Map HTML'))]),
        ),
    ]
