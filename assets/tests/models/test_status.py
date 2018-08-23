import uuid

from django.db import models

from assets.models import Status
from tests.test_case import AppTestCase


class TestModel(AppTestCase):

    # fields

    def test_id(self):
        field = Status._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_name(self):
        field = Status._meta.get_field('name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.unique)

    # meta

    def test_ordering(self):
        self.assertEqual(Status._meta.ordering, ['name'])

    # properties

    def test_str(self):
        self.assertEqual(Status(name='Status 1').__str__(), 'Status 1')
