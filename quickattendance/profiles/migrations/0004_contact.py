# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-21 09:20
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20170521_0852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_no', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), null=True, size=None)),
            ],
        ),
    ]
