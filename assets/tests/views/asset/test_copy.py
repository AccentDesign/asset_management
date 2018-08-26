from django.urls import reverse

from assets.models import Asset
from tests.test_case import AppTestCase


class TestUpdateView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.object = self.team1_asset
        self.url = reverse('assets:asset-copy', kwargs={'pk': self.object.pk})

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(reverse('login'), self.url)
        self.assertRedirects(response, expected_url, 302, 200)

    def test_user_with_no_active_team_redirects_home(self):
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'), 302, 200)

    def test_login_grants_access(self):
        self.client.force_login(self.team1.members.first())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_404_when_object_is_for_another_team(self):
        self.client.force_login(self.team2.members.first())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_can_copy(self):
        self.client.force_login(self.team1.members.first())
        post_data = {
            'new_name': 'some copied name',
            'parent_asset': self.object.pk
        }
        response = self.client.post(self.url, post_data)

        # was copied
        asset = Asset.objects.get(name=post_data['new_name'], parent_id=self.object.pk)

        # redirects to edit url
        self.assertRedirects(response, asset.get_absolute_url(), 302, 200)
