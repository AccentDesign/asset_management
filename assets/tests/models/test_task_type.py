import uuid
import mock

from django.db import models
from django.urls import reverse

from assets.models import TaskType
from assets.models.task_type import TaskTypeManager
from authentication.middleware.current_user import get_current_team
from authentication.models import Team
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_default_manager(self):
        self.assertTrue(isinstance(TaskType._default_manager, TaskTypeManager))

    def test_queryset_filters_by_team(self):
        with mock.patch('assets.models.task_type.get_current_team', return_value=self.team1):
            qs = TaskType.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().team, self.team1)

        with mock.patch('assets.models.task_type.get_current_team', return_value=self.team2):
            qs = TaskType.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().team, self.team2)


class TestModel(AppTestCase):

    # fields

    def test_id(self):
        field = TaskType._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_name(self):
        field = TaskType._meta.get_field('name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_team(self):
        field = TaskType._meta.get_field('team')
        self.assertModelPKField(field, Team, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_team)

    # meta

    def test_ordering(self):
        self.assertEqual(TaskType._meta.ordering, ['name'])

    # properties

    def test_str(self):
        self.assertEqual(TaskType(name='Type 1').__str__(), 'Type 1')

    def test_absolute_url(self):
        pk = 'fe8aa6e1-93b9-480e-bc82-fcce14b707f6'
        self.assertEqual(
            TaskType(pk=pk).get_absolute_url(),
            reverse('assets:task-type-update', kwargs={'pk': pk})
        )
