# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-04 08:44
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0008_auto_20161204_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name'),
        ),
    ]