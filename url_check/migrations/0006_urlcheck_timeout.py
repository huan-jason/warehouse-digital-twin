# Generated by Django 5.0.6 on 2024-06-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_check', '0005_urlcheck_notification_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlcheck',
            name='timeout',
            field=models.IntegerField(default=10),
        ),
    ]
