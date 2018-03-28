# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-28 09:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studeals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='place_latitude',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='offer',
            name='place_longitude',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=11),
        ),
        migrations.AlterField(
            model_name='offer',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]
