# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-25 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', jsonfield.fields.JSONField()),
            ],
        ),
    ]
