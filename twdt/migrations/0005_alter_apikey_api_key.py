# Generated by Django 5.0.6 on 2024-06-15 02:16

import twdt.models.apikey
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twdt', '0004_apikey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='api_key',
            field=models.CharField(blank=True, default=twdt.models.apikey.new_api_key, max_length=64, unique=True),
        ),
    ]
