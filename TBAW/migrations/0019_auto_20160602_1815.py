# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 22:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0018_auto_20160601_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='year',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_district',
            field=models.SmallIntegerField(choices=[(0, 'No District'), (1, 'Michigan'), (2, 'Mid-Atlantic'), (3, 'New England'), (4, 'Pacific Northwest'), (5, 'Indiana'), (6, 'Chesapeake'), (7, 'North Carolina'), (8, 'Georgia')], null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.SmallIntegerField(choices=[(0, 'Regional'), (1, 'District'), (2, 'District Championship'), (3, 'Championship Division'), (4, 'Championship Finals'), (99, 'Offseason'), (100, 'Preseason'), (-1, 'Unlabeled')], null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='year',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='robot',
            name='year',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='team',
            name='rookie_year',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_number',
            field=models.PositiveSmallIntegerField(),
        ),
    ]