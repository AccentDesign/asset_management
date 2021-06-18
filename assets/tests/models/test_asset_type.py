import uuid
import mock

from django.db import models
from django.urls import reverse

from assets.models import AssetType
from assets.models.asset_type import AssetTypeManager
from authentication.middleware.current_user import get_current_collection
from authentication.models import Collection
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_default_manager(self):
        self.assertTrue(isinstance(AssetType._default_manager, AssetTypeManager))

    def test_queryset_filters_by_collection(self):
        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection1):
            qs = AssetType.for_collection.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().collection, self.collection1)

        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection2):
            qs = AssetType.for_collection.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().collection, self.collection2)


class TestModel(AppTestCase):

    # fields

    def test_id(self):
        field = AssetType._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_name(self):
        field = AssetType._meta.get_field('name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_collection(self):
        field = AssetType._meta.get_field('collection')
        self.assertModelPKField(field, Collection, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_collection)

    # meta

    def test_ordering(self):
        self.assertEqual(AssetType._meta.ordering, ['name'])

    def test_unique_together(self):
        self.assertEqual(AssetType._meta.unique_together, (('collection', 'name', ), ))

    # properties

    def test_str(self):
        self.assertEqual(AssetType(name='Asset Type 1').__str__(), 'Asset Type 1')

    def test_absolute_url(self):
        pk = 'fe8aa6e1-93b9-480e-bc82-fcce14b707f6'
        self.assertEqual(
            AssetType(pk=pk).get_absolute_url(),
            reverse('assets:asset-type-update', kwargs={'pk': pk})
        )
