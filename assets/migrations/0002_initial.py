# Generated by Django 3.2.4 on 2021-06-07 10:01

import authentication.middleware.current_user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0001_initial'),
        ('authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktype',
            name='team',
            field=models.ForeignKey(default=authentication.middleware.current_user.get_current_collection, editable=False, on_delete=django.db.models.deletion.CASCADE, to='authentication.team'),
        ),
        migrations.AddField(
            model_name='taskpriority',
            name='team',
            field=models.ForeignKey(default=authentication.middleware.current_user.get_current_collection, editable=False, on_delete=django.db.models.deletion.CASCADE, to='authentication.team'),
        ),
        migrations.AddField(
            model_name='taskhistory',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assets.status'),
        ),
        migrations.AddField(
            model_name='taskhistory',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='assets.task'),
        ),
        migrations.AddField(
            model_name='taskhistory',
            name='user',
            field=models.ForeignKey(default=authentication.middleware.current_user.get_current_user, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='assets.asset'),
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='task_priority',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.taskpriority'),
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assets.tasktype'),
        ),
        migrations.AddField(
            model_name='contact',
            name='team',
            field=models.ForeignKey(default=authentication.middleware.current_user.get_current_collection, editable=False, on_delete=django.db.models.deletion.CASCADE, to='authentication.team'),
        ),
        migrations.AddField(
            model_name='assettype',
            name='team',
            field=models.ForeignKey(default=authentication.middleware.current_user.get_current_collection, editable=False, on_delete=django.db.models.deletion.CASCADE, to='authentication.team'),
        ),
        migrations.AddField(
            model_name='asset',
            name='asset_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.assettype'),
        ),
        migrations.AddField(
            model_name='asset',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.contact'),
        ),
        migrations.AddField(
            model_name='asset',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='assets.asset'),
        ),
        migrations.AddField(
            model_name='asset',
            name='team',
            field=models.ForeignKey(default=authentication.middleware.current_user.get_current_collection, editable=False, on_delete=django.db.models.deletion.CASCADE, to='authentication.team'),
        ),
        migrations.AlterUniqueTogether(
            name='tasktype',
            unique_together={('team', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='taskpriority',
            unique_together={('team', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='assettype',
            unique_together={('team', 'name')},
        ),
    ]
