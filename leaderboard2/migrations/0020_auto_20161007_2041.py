# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-08 00:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard2', '0019_leaderboard_operator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboard',
            name='operator',
            field=models.CharField(choices=[('+', '+'), ('-', '-'), ('*', '*'), ('/', '/')], default='+', max_length=10),
        ),
    ]
