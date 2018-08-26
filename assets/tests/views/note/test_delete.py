from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from assets.models import Note
from tests.test_case import AppTestCase


class TestDeleteView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.object = Note.objects.get(team=self.team1)
        self.url = reverse('assets:note-delete', kwargs={'pk': self.object.pk})

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

    def test_can_delete(self):
        self.client.force_login(self.team1.members.first())
        post_data = {}
        response = self.client.post(self.url, post_data)

        # was deleted
        with self.assertRaises(ObjectDoesNotExist):
            self.object.refresh_from_db()

        # redirects to edit url
        self.assertRedirects(response, reverse('assets:note-list'), 302, 200)
