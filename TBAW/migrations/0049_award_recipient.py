# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 23:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0048_auto_20160614_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TBAW.Team'),
        ),
    ]