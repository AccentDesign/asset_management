import uuid

from django.db import models
from django.urls import reverse

from authentication.middleware.current_user import get_current_user
from authentication.models import Collection, User
from tests.test_case import AppTestCase


class ModelTests(AppTestCase):

    # fields

    def test_id(self):
        field = Collection._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_title(self):
        field = Collection._meta.get_field('title')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.unique)

    def test_admin(self):
        field = Collection._meta.get_field('admin')
        self.assertModelPKField(field, User, null=True, blank=True, on_delete=models.SET_NULL)
        self.assertEqual(field.default, get_current_user)

    def test_members(self):
        field = Collection._meta.get_field('members')
        self.assertModelField(field, models.ManyToManyField, blank=True)
        self.assertEqual(field.remote_field.model, User)
        self.assertEqual(field.remote_field.related_name, 'collections')

    def test_guests(self):
        field = Collection._meta.get_field('guests')
        self.assertModelField(field, models.ManyToManyField, blank=True)
        self.assertEqual(field.remote_field.model, User)
        self.assertEqual(field.remote_field.related_name, 'guested_collections')

    def test_created_on(self):
        field = Collection._meta.get_field('created_on')
        self.assertModelField(field, models.DateTimeField, blank=True)
        self.assertFalse(field.editable)
        self.assertTrue(field.auto_now_add)

    # properties

    def test_str(self):
        self.assertEqual(Collection(title='Collection 1').__str__(), 'Collection 1')

    def test_absolute_url(self):
        pk = 'fe8aa6e1-93b9-480e-bc82-fcce14b707f6'
        self.assertEqual(
            Collection(pk=pk).get_absolute_url(),
            reverse('collection-update', kwargs={'pk': pk})
        )
