# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 00:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0005_auto_20160528_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='teams',
            field=models.ManyToManyField(to='TBAW.Team'),
        ),
    ]