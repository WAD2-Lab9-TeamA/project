# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-18 20:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studeals', '0005_auto_20180318_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='date_added',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]