# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 02:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0011_event_alliances'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='alliances',
            field=models.ManyToManyField(to='TBAW.Alliance'),
        ),
    ]
