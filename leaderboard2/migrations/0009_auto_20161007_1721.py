# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-07 21:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard2', '0008_scoringleaderboard_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scoringleaderboard',
            name='extra_field_1',
        ),
        migrations.RemoveField(
            model_name='scoringleaderboard',
            name='extra_field_2',
        ),
        migrations.RemoveField(
            model_name='scoringleaderboard',
            name='extra_field_3',
        ),
        migrations.RemoveField(
            model_name='scoringleaderboard',
            name='year',
        ),
    ]
