import uuid

from django.db import models

from assets.models import Status, Task, TaskHistory
from assets.models.task_history import TaskHistoryManager
from authentication.middleware.current_user import get_current_user
from authentication.models import User
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_default_manager(self):
        self.assertTrue(isinstance(TaskHistory._default_manager, TaskHistoryManager))


class TestModel(AppTestCase):

    # fields

    def test_id(self):
        field = TaskHistory._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_task(self):
        field = TaskHistory._meta.get_field('task')
        self.assertModelPKField(field, Task, on_delete=models.CASCADE)

    def test_notes(self):
        field = TaskHistory._meta.get_field('notes')
        self.assertModelField(field, models.TextField, blank=True)

    def test_status(self):
        field = TaskHistory._meta.get_field('status')
        self.assertModelPKField(field, Status, null=True, blank=True, on_delete=models.PROTECT)

    def test_user(self):
        field = TaskHistory._meta.get_field('user')
        self.assertModelPKField(field, User, null=True, on_delete=models.SET_NULL)
        self.assertFalse(field.editable)
        self.assertEqual(field.default, get_current_user)

    # meta

    def test_ordering(self):
        self.assertEqual(TaskHistory._meta.ordering, ['-date'])
