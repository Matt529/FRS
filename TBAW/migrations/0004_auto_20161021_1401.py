# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-21 18:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0003_auto_20161020_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alliance',
            name='backup',
        ),
        migrations.RemoveField(
            model_name='alliance',
            name='captain',
        ),
        migrations.RemoveField(
            model_name='alliance',
            name='first_pick',
        ),
        migrations.RemoveField(
            model_name='alliance',
            name='second_pick',
        ),
    ]
