# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=200)),
                ('credit_card_number', models.CharField(max_length=50, null=True)),
                ('credit_card_exp_date', models.CharField(max_length=50, null=True)),
                ('credit_card_csv', models.CharField(max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
