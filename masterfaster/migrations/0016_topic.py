# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-12 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterfaster', '0015_auto_20170413_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]