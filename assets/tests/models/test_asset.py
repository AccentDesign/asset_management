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
from authentication.middleware.current_user import get_current_team
from authentication.models import Team
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_inheritance(self):
        self.assertTrue(issubclass(AssetManager, TreeManager))

    def test_default_manager(self):
        self.assertTrue(isinstance(Asset._default_manager, AssetManager))

    def test_queryset_filters_by_team(self):
        asset_for_team_1 = Asset.objects.create(
            name='Root Asset',
            asset_type_id='1bd257c8-babe-4393-b15c-79be926a5805',
            team=self.team1
        )
        asset_for_team_2 = Asset.objects.create(
            name='Root Asset',
            asset_type_id='fe8aa6e1-93b9-480e-bc82-fcce14b707f6',
            team=self.team2
        )

        with mock.patch('assets.models.mixins.get_current_team', return_value=self.team1):
            qs = Asset.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get(), asset_for_team_1)

        with mock.patch('assets.models.mixins.get_current_team', return_value=self.team2):
            qs = Asset.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get(), asset_for_team_2)

    def test_search(self):
        Asset.objects.create(
            name='Root Asset',
            description='Some description',
            asset_type_id='1bd257c8-babe-4393-b15c-79be926a5805',
            contact_id='d7777b76-1e82-4adb-b98d-3961adec2f92',
            team=self.team1
        )

        search_terms = ['Root', 'Some', 'Contact One', 'Asset Type 1']

        with mock.patch('assets.models.mixins.get_current_team', return_value=self.team1):
            # blank returns all results
            self.assertEqual(Asset.for_team.search('').count(), 1)

            # found for team one when active
            for term in search_terms:
                self.assertEqual(Asset.for_team.search(term).count(), 1)

        with mock.patch('assets.models.mixins.get_current_team', return_value=self.team2):
            # not found for team two as not their asset
            for term in search_terms:
                self.assertEqual(Asset.for_team.search(term).count(), 0)


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

    def test_team(self):
        field = Asset._meta.get_field('team')
        self.assertModelPKField(field, Team, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_team)

    # properties

    def test_str(self):
        self.assertEqual(self.team1_asset.__str__(), 'Root Asset')

    def test_absolute_url(self):
        self.assertEqual(
            self.team1_asset.get_absolute_url(),
            reverse('assets:asset-update', kwargs={'pk': self.team1_asset.pk})
        )

    def test_nodes_url(self):
        self.assertEqual(
            self.team1_asset.get_nodes_url(),
            reverse('assets:asset-list-nodes', kwargs={'pk': self.team1_asset.pk})
        )

    def test_copy(self):
        Task.objects.create(
            asset=self.team1_asset,
            name='Task',
            task_type_id='03630124-7745-422f-8024-549de2f613b1',
            initial_due_date=datetime.today().date()
        )

        copied = self.team1_asset.copy(name='Foo', parent=self.team1_asset)

        self.assertEqual(Asset.objects.count(), 2)

        # copied under the chosen asset with chosen name
        self.assertEqual(copied.name, 'Foo')
        self.assertEqual(copied.parent, self.team1_asset)

        # other details remain the same
        self.assertEqual(copied.description, self.team1_asset.description)
        self.assertEqual(copied.asset_type, self.team1_asset.asset_type)
        self.assertEqual(copied.contact, self.team1_asset.contact)
        self.assertEqual(copied.team, self.team1_asset.team)

        # ensure tasks exist
        self.assertEqual(copied.tasks.count(), 1)
