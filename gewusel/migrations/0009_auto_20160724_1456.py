# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 12:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gewusel', '0008_auto_20160724_1416'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('name', 'country')]),
        ),
    ]
