import uuid
import mock

from django.db import models
from django.urls import reverse
from simplemde.fields import SimpleMDEField

from assets.models import File
from assets.models.file import FileManager
from authentication.middleware.current_user import get_current_team, get_current_user
from authentication.models import Team, User
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_default_manager(self):
        self.assertTrue(isinstance(File._default_manager, FileManager))

    def test_queryset_filters_by_team(self):
        assert self.team1_file
        with mock.patch('assets.models.file.get_current_team', return_value=self.team1):
            qs = File.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().team, self.team1)

        assert self.team2_file
        with mock.patch('assets.models.file.get_current_team', return_value=self.team2):
            qs = File.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().team, self.team2)


class TestModel(AppTestCase):

    # fields

    def test_id(self):
        field = File._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_file(self):
        field = File._meta.get_field('file')
        self.assertModelField(field, models.FileField)

    def test_uploaded_by(self):
        field = File._meta.get_field('uploaded_by')
        self.assertModelPKField(field, User, on_delete=models.CASCADE)
        self.assertFalse(field.editable)
        self.assertEqual(field.default, get_current_user)

    def test_uploaded_on(self):
        field = File._meta.get_field('uploaded_on')
        self.assertModelField(field, models.DateTimeField, blank=True)
        self.assertFalse(field.editable)
        self.assertTrue(field.auto_now_add)

    def test_team(self):
        field = File._meta.get_field('team')
        self.assertModelPKField(field, Team, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_team)
