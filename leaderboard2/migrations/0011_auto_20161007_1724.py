# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-07 21:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard2', '0010_auto_20161007_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scoringleaderboard2016',
            name='leaderboard_ptr',
        ),
        migrations.RemoveField(
            model_name='scoringleaderboard2016',
            name='scoring_models',
        ),
        migrations.DeleteModel(
            name='ScoringLeaderboard2016',
        ),
    ]
