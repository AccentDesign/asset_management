import uuid
import mock

from django.db import models
from django.urls import reverse

from assets.models import AssetType
from assets.models.asset_type import AssetTypeManager
from authentication.middleware.current_user import get_current_team
from authentication.models import Team
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.team1 = Team.objects.get(pk='8b52b24a-84c9-40ff-9d19-e09845e1a44c')
        self.team2 = Team.objects.get(pk='0d9cdca5-16f0-4128-95fd-24690a50695a')

    def test_default_manager(self):
        self.assertTrue(isinstance(AssetType._default_manager, AssetTypeManager))

    def test_queryset_filters_by_team(self):
        with mock.patch('assets.models.asset_type.get_current_team', return_value=self.team1):
            qs = AssetType.objects.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().team, self.team1)

        with mock.patch('assets.models.asset_type.get_current_team', return_value=self.team2):
            qs = AssetType.objects.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().team, self.team2)


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

    def test_team(self):
        field = AssetType._meta.get_field('team')
        self.assertModelPKField(field, Team, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_team)

    # meta

    def test_ordering(self):
        self.assertEqual(AssetType._meta.ordering, ['name'])

    def test_unique_together(self):
        self.assertEqual(AssetType._meta.unique_together, (('team', 'name', ), ))

    # properties

    def test_str(self):
        self.assertEqual(AssetType(name='Asset Type 1').__str__(), 'Asset Type 1')

    def test_absolute_url(self):
        pk = 'fe8aa6e1-93b9-480e-bc82-fcce14b707f6'
        self.assertEqual(
            AssetType(pk=pk).get_absolute_url(),
            reverse('assets:asset-type-update', kwargs={'pk': pk})
        )
