# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-12-01 10:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_abc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='abc',
        ),
    ]
