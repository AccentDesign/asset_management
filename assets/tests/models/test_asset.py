from datetime import datetime
import uuid
import mock

from django.db import models
from django.urls import reverse

from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from assets.models import Asset, AssetType, Contact, Task
from assets.models.asset import AssetManager
from authentication.middleware.current_user import get_current_collection
from authentication.models import Collection
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_inheritance(self):
        self.assertTrue(issubclass(AssetManager, TreeManager))

    def test_default_manager(self):
        self.assertTrue(isinstance(Asset._default_manager, AssetManager))

    def test_queryset_filters_by_collection(self):
        asset_for_collection_1 = Asset.objects.create(
            name='Root Asset',
            asset_type_id='1bd257c8-babe-4393-b15c-79be926a5805',
            collection=self.collection1
        )
        asset_for_collection_2 = Asset.objects.create(
            name='Root Asset',
            asset_type_id='fe8aa6e1-93b9-480e-bc82-fcce14b707f6',
            collection=self.collection2
        )

        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection1):
            qs = Asset.for_collection.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get(), asset_for_collection_1)

        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection2):
            qs = Asset.for_collection.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get(), asset_for_collection_2)

    def test_search(self):
        Asset.objects.create(
            name='Root Asset',
            description='Some description',
            asset_type_id='1bd257c8-babe-4393-b15c-79be926a5805',
            contact_id='d7777b76-1e82-4adb-b98d-3961adec2f92',
            collection=self.collection1
        )

        search_terms = ['Root', 'Some', 'Contact One', 'Asset Type 1']

        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection1):
            # blank returns all results
            self.assertEqual(Asset.for_collection.search('').count(), 1)

            # found for collection one when active
            for term in search_terms:
                self.assertEqual(Asset.for_collection.search(term).count(), 1)

        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection2):
            # not found for collection two as not their asset
            for term in search_terms:
                self.assertEqual(Asset.for_collection.search(term).count(), 0)


class TestModel(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_inheritance(self):
        self.assertTrue(issubclass(Asset, MPTTModel))

    # fields

    def test_id(self):
        field = Asset._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_name(self):
        field = Asset._meta.get_field('name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_description(self):
        field = Asset._meta.get_field('description')
        self.assertModelField(field, models.TextField, blank=True)

    def test_asset_type(self):
        field = Asset._meta.get_field('asset_type')
        self.assertModelPKField(field, AssetType, null=True, blank=True, on_delete=models.PROTECT)

    def test_contact(self):
        field = Asset._meta.get_field('contact')
        self.assertModelPKField(field, Contact, null=True, blank=True, on_delete=models.PROTECT)

    def test_parent(self):
        field = Asset._meta.get_field('parent')
        self.assertModelField(field, TreeForeignKey, null=True, blank=True)
        self.assertEqual(field.remote_field.model, Asset)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_collection(self):
        field = Asset._meta.get_field('collection')
        self.assertModelPKField(field, Collection, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_collection)

    # properties

    def test_str(self):
        self.assertEqual(self.collection1_asset.__str__(), 'Root Asset')

    def test_absolute_url(self):
        self.assertEqual(
            self.collection1_asset.get_absolute_url(),
            reverse('assets:asset-update', kwargs={'pk': self.collection1_asset.pk})
        )

    def test_nodes_url(self):
        self.assertEqual(
            self.collection1_asset.get_nodes_url(),
            reverse('assets:asset-list-nodes', kwargs={'pk': self.collection1_asset.pk})
        )

    def test_copy(self):
        Task.objects.create(
            asset=self.collection1_asset,
            name='Task',
            task_type_id='03630124-7745-422f-8024-549de2f613b1',
            initial_due_date=datetime.today().date()
        )

        copied = self.collection1_asset.copy(name='Foo', parent=self.collection1_asset)

        self.assertEqual(Asset.objects.count(), 2)

        # copied under the chosen asset with chosen name
        self.assertEqual(copied.name, 'Foo')
        self.assertEqual(copied.parent, self.collection1_asset)

        # other details remain the same
        self.assertEqual(copied.description, self.collection1_asset.description)
        self.assertEqual(copied.asset_type, self.collection1_asset.asset_type)
        self.assertEqual(copied.contact, self.collection1_asset.contact)
        self.assertEqual(copied.collection, self.collection1_asset.collection)

        # ensure tasks exist
        self.assertEqual(copied.tasks.count(), 1)
