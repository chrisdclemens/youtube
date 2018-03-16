# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-08 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=100)),
                ('length', models.IntegerField(default=0)),
                ('year', models.IntegerField(default=0)),
                ('genres', models.CharField(max_length=200)),
            ],
        ),
    ]
