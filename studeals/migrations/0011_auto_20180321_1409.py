# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-21 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studeals', '0010_auto_20180321_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='picture',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='img',
            field=models.CharField(default='media/profile_images/default.jpg', max_length=200),
        ),
    ]
