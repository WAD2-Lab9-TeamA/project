# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-22 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studeals', '0013_auto_20180321_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='date_added',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='offer',
            name='expiration_date',
            field=models.DateField(),
        ),
    ]
