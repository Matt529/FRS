# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-28 19:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alliance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('award_type', models.CharField(max_length=120)),
                ('year', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=500)),
                ('short_name', models.CharField(max_length=120, null=True)),
                ('event_code', models.CharField(max_length=7)),
                ('event_type', models.IntegerField(choices=[(0, 'Regional'), (1, 'District'), (2, 'District Championship'), (3, 'Championship Division'), (4, 'Championship Finals'), (99, 'Offseason'), (100, 'Preseason'), (-1, 'Unlabeled')])),
                ('event_district', models.IntegerField(choices=[(0, 'No District'), (1, 'Michigan'), (2, 'Mid-Atlantic'), (3, 'New England'), (4, 'Pacific Northwest'), (5, 'Indiana'), (6, 'Chesapeake'), (7, 'North Carolina'), (8, 'Georgia')])),
                ('year', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=120)),
                ('venue_address', models.TextField()),
                ('timezone', models.CharField(max_length=20)),
                ('website', models.URLField(null=True)),
                ('official', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20)),
                ('comp_level', models.CharField(max_length=6)),
                ('set_number', models.CharField(max_length=20, null=True)),
                ('match_number', models.CharField(max_length=20)),
                ('time_string', models.CharField(max_length=25)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TBAW.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Robot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=13)),
                ('year', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField()),
                ('name', models.TextField()),
                ('locality', models.CharField(max_length=120)),
                ('region', models.CharField(max_length=120)),
                ('country_name', models.CharField(max_length=120)),
                ('location', models.CharField(max_length=500)),
                ('team_number', models.PositiveIntegerField()),
                ('key', models.CharField(max_length=8)),
                ('nickname', models.CharField(max_length=120)),
                ('rookie_year', models.PositiveIntegerField()),
                ('motto', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='award',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TBAW.Event'),
        ),
    ]