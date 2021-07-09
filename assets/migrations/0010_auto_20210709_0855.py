# Generated by Django 3.2.5 on 2021-07-09 07:55

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_assetfile'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='asset',
            index=django.contrib.postgres.indexes.GinIndex(fields=['extra_data'], name='extra_data_gin'),
        ),
        migrations.AddIndex(
            model_name='assettype',
            index=django.contrib.postgres.indexes.GinIndex(fields=['fields'], name='fields_gin'),
        ),
    ]