# Generated by Django 2.0.7 on 2018-07-20 20:23

import assets.middleware.current_user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_auto_20180720_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskhistory',
            name='user',
            field=models.ForeignKey(default=assets.middleware.current_user.get_current_user, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
