# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-24 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0006_auto_20161023_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_number',
            field=models.PositiveSmallIntegerField(db_index=True),
        ),
    ]
