# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 07:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0007_auto_20170513_0718'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={},
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='taken_by',
            new_name='last_modified_by',
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([('session_id', 'user')]),
        ),
    ]
