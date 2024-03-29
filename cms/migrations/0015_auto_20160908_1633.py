# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-08 15:33


from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0014_auto_20160623_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpostcarouselitem',
            name='copyright',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='eventpagecarouselitem',
            name='copyright',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepagecarouselitem',
            name='copyright',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='richtextpagecarouselitem',
            name='copyright',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
