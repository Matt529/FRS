# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-20 00:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0076_auto_20161019_1938'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankingModel2010',
            fields=[
                ('rankingmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TBAW.RankingModel')),
                ('seeding_score', models.PositiveSmallIntegerField(null=True)),
                ('coopertition_bonus', models.PositiveSmallIntegerField(null=True)),
                ('hanging_points', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('TBAW.rankingmodel',),
        ),
        migrations.CreateModel(
            name='RankingModel2011',
            fields=[
                ('rankingmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TBAW.RankingModel')),
                ('qual_score', models.PositiveSmallIntegerField(null=True)),
                ('ranking_score', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('TBAW.rankingmodel',),
        ),
        migrations.CreateModel(
            name='RankingModel2012',
            fields=[
                ('rankingmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TBAW.RankingModel')),
                ('qual_score', models.PositiveSmallIntegerField(null=True)),
                ('auton_points', models.PositiveSmallIntegerField(null=True)),
                ('bridge_points', models.PositiveSmallIntegerField(null=True)),
                ('teleop_points', models.PositiveSmallIntegerField(null=True)),
                ('coopertition_points', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('TBAW.rankingmodel',),
        ),
        migrations.CreateModel(
            name='RankingModel2013',
            fields=[
                ('rankingmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TBAW.RankingModel')),
                ('qual_score', models.PositiveSmallIntegerField(null=True)),
                ('climb_points', models.PositiveSmallIntegerField(null=True)),
                ('auton_points', models.PositiveSmallIntegerField(null=True)),
                ('teleop_points', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('TBAW.rankingmodel',),
        ),
    ]
