# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterfaster', '0011_auto_20170320_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='credit_card_exp_date',
        ),
        migrations.AddField(
            model_name='user',
            name='credit_card_exp_date_month',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='credit_card_exp_date_year',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
