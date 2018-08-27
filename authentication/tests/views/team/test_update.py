from django.urls import reverse

from tests.test_case import AppTestCase


class TestCreateView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.object = self.team1
        self.url = reverse('team-update', kwargs={'pk': self.object.pk})

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(reverse('login'), self.url)
        self.assertRedirects(response, expected_url, 302, 200)

    def test_login_grants_access_for_admin(self):
        self.client.force_login(self.team1.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_access(self):
        user = self.create_user()
        self.team1.members.add(user)
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_admin_can_update(self):
        self.client.force_login(self.team1.admin)
        post_data = {
            'title': 'some edited title'
        }
        response = self.client.post(self.url, post_data)

        # was updated
        self.object.refresh_from_db()
        self.assertEqual(self.object.title, post_data['title'])

        # redirects to home
        self.assertRedirects(response, reverse('home'), 302, 200)
