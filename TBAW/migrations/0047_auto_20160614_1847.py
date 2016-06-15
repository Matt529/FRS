# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TBAW', '0046_auto_20160611_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='award_type',
            field=models.CharField(choices=[(0, "Chairman's"), (1, 'Winner'), (2, 'Finalist'), (3, 'Woodie Flowers'), (4, "Dean's List"), (5, 'Volunteer'), (6, 'Founders'), (7, 'Bart Kamen Memorial'), (8, 'Make It Loud'), (9, 'Engineering Inspiration'), (10, 'Rookie All Star'), (11, 'Gracious Professionalism'), (12, 'Coopertition'), (13, 'Judges'), (14, 'Highest Rookie Seed'), (15, 'Rookie Inspiration'), (16, 'Industrial Design'), (17, 'Quality'), (18, 'Safety'), (19, 'Sportsmanship'), (20, 'Creativity'), (21, 'Engineering Excellence'), (22, 'Entrepreneurship'), (23, 'Excellence in Design'), (24, 'Excellence in Design (CAD)'), (25, 'Excellence in Design (Animation)'), (26, "Driving Tomorrow's Technology"), (27, 'Imagery'), (28, 'Media and Technology'), (29, 'Innovation in Control'), (30, 'Spirit'), (31, 'Website'), (32, 'Visualization'), (33, 'Autodesk Inventor'), (34, 'Future Innovator'), (35, 'Recognition of Extraordinary Service'), (36, 'Outstanding Cart'), (37, 'WSU Aim Higher'), (38, 'Leadership in Control'), (39, 'Number 1 Seed'), (40, 'Incredible Play'), (41, "People's Choice Animation"), (42, 'Rising Star Visualization'), (43, 'Best Offensive Round'), (44, 'Best Play of the Day'), (45, 'Featherweight in the Finals'), (46, 'Most Photogenic'), (47, 'Outstanding Defense'), (48, 'Power to Simplify'), (49, 'Against All Odds'), (50, 'Rising Star'), (51, "Chairman's Honorable Mention"), (52, 'Content Communication Honorable Mention'), (53, 'Technical Execution Honorable Mention'), (54, 'Realization'), (55, 'Realization Honorable Mention'), (56, 'Design Your Future'), (57, 'Design Your Future Honorable Mention'), (58, 'Special Recognition Character Animation'), (59, 'High Score'), (60, 'Teacher Pioneer'), (61, 'Best Craftsmanship'), (62, 'Best Defensive Match'), (63, 'Play of the Day'), (64, 'Programming'), (65, 'Professionalism'), (66, 'Golden Corndog'), (67, 'Most Improved Team'), (68, 'Wildcard')], max_length=100),
        ),
    ]
