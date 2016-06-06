# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 23:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0033_rankingmodel_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankingModel2016',
            fields=[
                ('rankingmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TBAW.RankingModel')),
                ('ranking_score', models.PositiveSmallIntegerField(null=True)),
                ('auton_points', models.PositiveSmallIntegerField(null=True)),
                ('scale_challenge_points', models.PositiveSmallIntegerField(null=True)),
                ('goals_points', models.PositiveSmallIntegerField(null=True)),
                ('defense_points', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('TBAW.rankingmodel',),
        ),
    ]
