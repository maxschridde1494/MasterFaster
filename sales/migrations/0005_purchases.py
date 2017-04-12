# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 23:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales', '0004_auto_20170327_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('size', models.CharField(max_length=100)),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Product')),
                ('sale_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
