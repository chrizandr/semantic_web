# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_delete_graphmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owl',
            name='userid',
            field=models.IntegerField(default=-1),
        ),
    ]
