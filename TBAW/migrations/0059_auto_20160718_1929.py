# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-18 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0058_auto_20160718_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='rankingmodel',
            name='playoff_losses',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rankingmodel',
            name='playoff_wins',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
