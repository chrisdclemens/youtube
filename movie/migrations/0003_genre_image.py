# Generated by Django 2.0.3 on 2018-03-09 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20180308_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='image',
            field=models.CharField(default='', max_length=100),
        ),
    ]
