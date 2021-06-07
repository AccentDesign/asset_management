from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.test import TestCase

from assets.models import Asset, AssetType, Task, TaskType, File
from authentication.models import User, Team


class AppTestCase(TestCase):

    def create_user(self, email='user@example.com', password='password', **extra_fields):
        return User.objects.create_user(email, password, **extra_fields)

    def create_superuser(self, email='user@example.com', password='password', **extra_fields):
        return User.objects.create_superuser(email, password, **extra_fields)

    _non_blankable_fields = [
        models.BooleanField
    ]

    def assertModelField(self, field, expected_class, null=False, blank=False, default=None):
        self.assertEqual(field.__class__, expected_class)
        self.assertEqual(field.null, null)
        if expected_class not in self._non_blankable_fields:
            self.assertEqual(field.blank, blank)

        if default:
            self.assertEqual(field.default, default)

    def assertModelDecimalField(self, field, max_digits, decimal_places, null=False, blank=False):
        self.assertEqual(field.__class__, models.DecimalField)
        self.assertEqual(field.max_digits, max_digits)
        self.assertEqual(field.decimal_places, decimal_places)
        self.assertEqual(field.null, null)
        self.assertEqual(field.blank, blank)

    def assertModelPKField(self, field, rel_to, on_delete, null=False, blank=False, related_name=None):
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertEqual(field.remote_field.model, rel_to)
        self.assertEqual(field.remote_field.on_delete, on_delete)
        self.assertEqual(field.null, null)
        self.assertEqual(field.blank, blank)

        if related_name:
            self.assertEqual(field.remote_field.related_name, related_name)

    # qs helpers

    @property
    def team1(self):
        return Team.objects.get(pk='8b52b24a-84c9-40ff-9d19-e09845e1a44c')

    @property
    def team2(self):
        return Team.objects.get(pk='0d9cdca5-16f0-4128-95fd-24690a50695a')

    @property
    def team1_asset(self):
        asset_type = AssetType.objects.get(team=self.team1)
        return Asset.objects.get_or_create(
            name='Root Asset',
            asset_type=asset_type,
            team=self.team1
        )[0]

    @property
    def team2_asset(self):
        asset_type = AssetType.objects.get(team=self.team2)
        return Asset.objects.get_or_create(
            name='Root Asset',
            asset_type=asset_type,
            team=self.team2
        )[0]

    @property
    def team1_task(self):
        task_type = TaskType.objects.get(team=self.team1)
        return Task.objects.get_or_create(
            name='Task 1',
            task_type=task_type,
            asset=self.team1_asset,
            initial_due_date=datetime.today().date(),
            assigned_to=self.team1.members.first()
        )[0]

    @property
    def team2_task(self):
        task_type = TaskType.objects.get(team=self.team2)
        return Task.objects.get_or_create(
            name='Task 1',
            task_type=task_type,
            asset=self.team2_asset,
            initial_due_date=datetime.today().date(),
            assigned_to=self.team2.members.first()
        )[0]

    @property
    def team1_file(self):
        return File.objects.get_or_create(
            file=self.get_temporary_image(),
            team=self.team1,
            uploaded_by=self.team1.members.first()
        )[0]

    @property
    def team2_file(self):
        return File.objects.get_or_create(
            file=self.get_temporary_image(),
            team=self.team2,
            uploaded_by=self.team2.members.first()
        )[0]

    def get_temporary_image(self):
        image_file = SimpleUploadedFile('file.jpg', b"file_content", content_type='image/jpeg')
        return image_file
