# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 09:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gewusel', '0003_game_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='points',
            name='datetime_entered',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 5, 9, 9, 52, 2504, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
