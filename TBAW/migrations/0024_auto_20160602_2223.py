# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 02:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0023_auto_20160602_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scoringmodel2016',
            old_name='blue_defense_1_crossed_count',
            new_name='blue_defense_1_cross_count',
        ),
        migrations.RenameField(
            model_name='scoringmodel2016',
            old_name='blue_defense_3_crossed_count',
            new_name='blue_defense_3_cross_count',
        ),
    ]
