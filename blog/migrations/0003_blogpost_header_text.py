# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='header_text',
            field=models.TextField(null=True),
        ),
    ]
