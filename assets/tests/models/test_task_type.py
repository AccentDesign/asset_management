import uuid
import mock

from django.db import models
from django.urls import reverse

from assets.models import TaskType
from assets.models.task_type import TaskTypeManager
from authentication.middleware.current_user import get_current_collection
from authentication.models import Collection
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_default_manager(self):
        self.assertTrue(isinstance(TaskType._default_manager, TaskTypeManager))

    def test_queryset_filters_by_collection(self):
        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection1):
            qs = TaskType.for_collection.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().collection, self.collection1)

        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection2):
            qs = TaskType.for_collection.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().collection, self.collection2)


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

    def test_collection(self):
        field = TaskType._meta.get_field('collection')
        self.assertModelPKField(field, Collection, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_collection)

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
