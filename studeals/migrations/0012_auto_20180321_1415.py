# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-21 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studeals', '0011_auto_20180321_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='img',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default='media/profile_images/default.jpg', upload_to='media/profile_images'),
        ),
    ]