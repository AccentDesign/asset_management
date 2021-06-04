import uuid
import mock

from django.db import models
from django.urls import reverse

from assets.models import TaskPriority
from assets.models.task_priority import TaskPriorityManager
from authentication.middleware.current_user import get_current_team
from authentication.models import Team
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_default_manager(self):
        self.assertTrue(isinstance(TaskPriority._default_manager, TaskPriorityManager))

    def test_queryset_filters_by_team(self):
        with mock.patch('assets.models.task_priority.get_current_team', return_value=self.team1):
            qs = TaskPriority.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().team, self.team1)

        with mock.patch('assets.models.task_priority.get_current_team', return_value=self.team2):
            qs = TaskPriority.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().team, self.team2)


class TestModel(AppTestCase):

    # fields

    def test_id(self):
        field = TaskPriority._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_name(self):
        field = TaskPriority._meta.get_field('name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_team(self):
        field = TaskPriority._meta.get_field('team')
        self.assertModelPKField(field, Team, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_team)

    # meta

    def test_ordering(self):
        self.assertEqual(TaskPriority._meta.ordering, ['display_order'])

    # properties

    def test_str(self):
        self.assertEqual(TaskPriority(name='Priority 1').__str__(), 'Priority 1')

    def test_absolute_url(self):
        pk = 'fe8aa6e1-93b9-480e-bc82-fcce14b707f6'
        self.assertEqual(
            TaskPriority(pk=pk).get_absolute_url(),
            reverse('assets:task-priority-update', kwargs={'pk': pk})
        )
