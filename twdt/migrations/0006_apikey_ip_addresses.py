# Generated by Django 5.0.6 on 2024-06-15 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twdt', '0005_alter_apikey_api_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='ip_addresses',
            field=models.JSONField(blank=True, null=True),
        ),
    ]