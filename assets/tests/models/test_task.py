import uuid
from datetime import date

import mock
from dateutil.rrule import DAILY, WEEKLY, MONTHLY, YEARLY

from django.db import models
from django.urls import reverse

from assets.models import Asset, Task, TaskPriority, TaskType
from assets.models.task import TaskManager
from authentication.models import Team, User
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_default_manager(self):
        self.assertTrue(isinstance(Task._default_manager, TaskManager))

    def test_queryset_filters_by_team(self):
        Task.objects.create(
            name='Task 1',
            task_type_id='03630124-7745-422f-8024-549de2f613b1',
            asset=self.team1_asset,
            initial_due_date=date(2018, 1, 1)
        )
        Task.objects.create(
            name='Task',
            task_type_id='22f9d510-7ffc-4ed1-adf7-d511a79ecab1',
            asset=self.team2_asset,
            initial_due_date=date(2018, 1, 1)
        )

        with mock.patch('assets.models.task.get_current_team', return_value=self.team1):
            qs = Task.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().asset.team, self.team1)

        with mock.patch('assets.models.task.get_current_team', return_value=self.team2):
            qs = Task.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().asset.team, self.team2)

    def test_search(self):
        Task.objects.create(
            name='Task 1',
            task_type_id='03630124-7745-422f-8024-549de2f613b1',
            asset=self.team1_asset,
            initial_due_date=date(2018, 1, 1)
        )

        search_terms = ['Task', 'Root Asset', 'Task Type 1']

        with mock.patch('assets.models.task.get_current_team', return_value=self.team1):
            # blank returns all results
            self.assertEqual(Task.for_team.search('').count(), 1)

            # found for team one when active
            for term in search_terms:
                self.assertEqual(Task.for_team.search(term).count(), 1)

        with mock.patch('assets.models.task.get_current_team', return_value=self.team2):
            # not found for team two as not their task
            for term in search_terms:
                self.assertEqual(Task.for_team.search(term).count(), 0)


class TestModel(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    # fields

    def test_id(self):
        field = Task._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_name(self):
        field = Task._meta.get_field('name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_description(self):
        field = Task._meta.get_field('description')
        self.assertModelField(field, models.TextField, blank=True)

    def test_task_type(self):
        field = Task._meta.get_field('task_type')
        self.assertModelPKField(field, TaskType, on_delete=models.PROTECT)

    def test_asset(self):
        field = Task._meta.get_field('asset')
        self.assertModelPKField(field, Asset, on_delete=models.CASCADE)

    def test_assigned_to(self):
        field = Task._meta.get_field('assigned_to')
        self.assertModelPKField(field, User, null=True, blank=True, on_delete=models.SET_NULL)

    def test_task_priority(self):
        field = Task._meta.get_field('task_priority')
        self.assertModelPKField(field, TaskPriority, null=True, blank=True, on_delete=models.SET_NULL)

    def test_initial_due_date(self):
        field = Task._meta.get_field('initial_due_date')
        self.assertModelField(field, models.DateField)

    def test_repeat_interval(self):
        field = Task._meta.get_field('repeat_interval')
        self.assertModelField(field, models.IntegerField, null=True, blank=True)

    def test_repeat_frequency(self):
        field = Task._meta.get_field('repeat_frequency')
        self.assertModelField(field, models.IntegerField, null=True, blank=True)
        self.assertEqual(
            field.choices,
            (
                (DAILY, 'Day(s)'),
                (WEEKLY, 'Week(s)'),
                (MONTHLY, 'Month(s)'),
                (YEARLY, 'Year(s)'),
            )
        )

    def test_repeat_until(self):
        field = Task._meta.get_field('repeat_until')
        self.assertModelField(field, models.DateField, null=True, blank=True)

    def test_due_date(self):
        field = Task._meta.get_field('due_date')
        self.assertModelField(field, models.DateField, null=True)
        self.assertFalse(field.editable)

    # properties

    def test_str(self):
        self.assertEqual(Task(name='Task').__str__(), 'Task')

    def test_absolute_url(self):
        pk = 'fe8aa6e1-93b9-480e-bc82-fcce14b707f6'
        self.assertEqual(
            Task(pk=pk).get_absolute_url(),
            reverse('assets:task-update', kwargs={'pk': pk})
        )

    def test_schedule_text(self):
        task = self.team1_task

        self.assertIsNone(task.schedule_text)

        task.repeat_interval = 7
        task.repeat_frequency = DAILY
        task.save()

        self.assertEqual(task.schedule_text, 'Every 7 Day(s)')
