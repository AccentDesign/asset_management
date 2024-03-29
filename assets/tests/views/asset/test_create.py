from django.urls import reverse

from assets.models import Asset
from tests.test_case import AppTestCase


class TestCreateView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.url = reverse('assets:asset-create')

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(reverse('login'), self.url)
        self.assertRedirects(response, expected_url, 302, 200)

    def test_user_with_no_active_collection_redirects_home(self):
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'), 302, 200)

    def test_login_grants_access(self):
        self.client.force_login(self.collection1.members.first())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_can_create(self):
        self.client.force_login(self.collection1.members.first())
        post_data = {
            'name': 'some name',
            'asset_type': self.collection1_asset.asset_type_id,
        }
        response = self.client.post(self.url, post_data)

        # was created for correct collection
        Asset.objects.get(
            name=post_data['name'],
            asset_type_id=post_data['asset_type'],
            collection=self.collection1
        )

        # redirects to root nodes url when no parent
        self.assertRedirects(response, reverse('assets:asset-list'), 302, 200)

    def test_invalid_form_stays_on_url(self):
        self.client.force_login(self.collection1.members.first())
        post_data = {
            'name': '',
        }
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
