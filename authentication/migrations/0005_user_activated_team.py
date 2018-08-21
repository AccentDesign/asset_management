# Generated by Django 2.1 on 2018-08-21 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activated_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.Team'),
        ),
    ]