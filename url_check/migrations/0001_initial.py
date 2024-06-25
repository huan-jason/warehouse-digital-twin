# Generated by Django 5.0.6 on 2024-06-25 06:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UrlCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=64)),
                ('url', models.URLField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('status_code', models.IntegerField(blank=True, default=200, null=True)),
                ('check_text', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UrlGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UrlCheckFailure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now=True, db_index=True)),
                ('remarks', models.TextField()),
                ('status_code', models.IntegerField()),
                ('url_check', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='url_check.urlcheck')),
            ],
        ),
        migrations.AddField(
            model_name='urlcheck',
            name='url_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='url_check.urlgroup'),
        ),
    ]