# Generated by Django 3.2.4 on 2021-06-25 12:16

import assets.models.asset_file
import authentication.middleware.current_user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0008_auto_20210622_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=assets.models.asset_file.get_upload_path)),
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='assets.asset')),
                ('uploaded_by', models.ForeignKey(default=authentication.middleware.current_user.get_current_user, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['file'],
            },
            managers=[
                ('for_collection', django.db.models.manager.Manager()),
            ],
        ),
    ]
