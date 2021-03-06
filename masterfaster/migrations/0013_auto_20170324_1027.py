# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-24 17:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterfaster', '0012_auto_20170322_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, null=True)),
                ('exp_date_month', models.CharField(max_length=10, null=True)),
                ('exp_date_year', models.CharField(max_length=10, null=True)),
                ('csv', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='credit_card_csv',
        ),
        migrations.RemoveField(
            model_name='user',
            name='credit_card_exp_date_month',
        ),
        migrations.RemoveField(
            model_name='user',
            name='credit_card_exp_date_year',
        ),
        migrations.RemoveField(
            model_name='user',
            name='credit_card_number',
        ),
        migrations.AddField(
            model_name='creditcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
