# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 21:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0015_auto_20160531_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='blue_foul_count',
        ),
        migrations.RemoveField(
            model_name='match',
            name='blue_total_autonomous_points',
        ),
        migrations.RemoveField(
            model_name='match',
            name='blue_total_foul_points',
        ),
        migrations.RemoveField(
            model_name='match',
            name='blue_total_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='blue_total_teleop_points',
        ),
        migrations.RemoveField(
            model_name='match',
            name='red_foul_count',
        ),
        migrations.RemoveField(
            model_name='match',
            name='red_total_autonomous_points',
        ),
        migrations.RemoveField(
            model_name='match',
            name='red_total_foul_points',
        ),
        migrations.RemoveField(
            model_name='match',
            name='red_total_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='red_total_teleop_points',
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='TBAW.Alliance'),
        ),
    ]