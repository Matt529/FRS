# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-18 23:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0059_auto_20160718_1929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alliance',
            name='color',
        ),
        migrations.RemoveField(
            model_name='rankingmodel',
            name='playoff_losses',
        ),
        migrations.RemoveField(
            model_name='rankingmodel',
            name='playoff_wins',
        ),
    ]
