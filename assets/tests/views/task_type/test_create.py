from django.urls import reverse

from assets.models import TaskType
from tests.test_case import AppTestCase


class TestCreateView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.url = reverse('assets:task-type-create')

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

    def test_can_create(self):
        self.client.force_login(self.team1.members.first())
        post_data = {
            'name': 'some name'
        }
        response = self.client.post(self.url, post_data)

        # was created for correct team
        TaskType.objects.get(name=post_data['name'], team=self.team1)

        # redirects to edit url
        self.assertRedirects(response, reverse('assets:task-type-list'), 302, 200)
