import uuid
import mock

from django.db import models
from django.urls import reverse

from assets.models import TaskPriority
from assets.models.task_priority import TaskPriorityManager
from authentication.middleware.current_user import get_current_collection
from authentication.models import Collection
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_default_manager(self):
        self.assertTrue(isinstance(TaskPriority._default_manager, TaskPriorityManager))

    def test_queryset_filters_by_collection(self):
        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection1):
            qs = TaskPriority.for_collection.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().collection, self.collection1)

        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection2):
            qs = TaskPriority.for_collection.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().collection, self.collection2)


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

    def test_badge_colour(self):
        field = TaskPriority._meta.get_field('badge_colour')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 7)

    def test_font_colour(self):
        field = TaskPriority._meta.get_field('font_colour')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 7)

    def test_collection(self):
        field = TaskPriority._meta.get_field('collection')
        self.assertModelPKField(field, Collection, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_collection)

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
