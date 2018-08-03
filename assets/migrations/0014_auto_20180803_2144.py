# Generated by Django 2.1 on 2018-08-03 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0013_auto_20180802_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='contact',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='contact',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='contact',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
